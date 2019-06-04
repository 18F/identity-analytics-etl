import os, boto3
from datetime import date

cloud_watch_logs = boto3.client('logs')
s3 = boto3.client('s3')

query_start_date, query_end_date = calculate_query_dates()

event_log_stream = os.environ["EVENT_LOG_STREAM"]

base_query_string = ('stats count_distinct(properties.user_id) as Users' #Count new distinct users
                     '%s' #Placeholder for the groupby
                     '| filter (name="OpenID Connect: authorization request" and properties.event_properties.success=1)' #Authenications
                     ' or (name="SAML Auth" and properties.event_properties.success=1)' #saml auth
                     ' or (name="User registration: complete")' #New Users
                     '| filter properties.service_provider like /urn/' #Exclude those without SP
                     '| sort ServiceProvider asc') #Sort on SP name


sp_mfa_or_new_signup_query_string = (base_query_string % (
    'by properties.service_provider as ServiceProvider'))
sp_by_event_query_string = (base_query_string % (
    'by properties.service_provider as ServiceProvider, name as Event'))

sp_unique_users = run_query(sp_mfa_or_new_signup_query_string)
sp_by_event_query_string = run_query(sp_by_event_query_string)
parse_results(sp_unique_users, sp_by_event_query_string)


def calculate_query_dates():
    today = date.today()
    startdate_month = today.month - 1
    startdate_year = today.year
    if startdate_month == "01":
        startdate_month = 12
        startdate_year = today.year - 1
    start_date = date(startdate_month, startdate_year , 1)
    end_date = date(today.year, today.month, 1)
    return start_date, end_date

def run_query(query_string):
    query_id = cloud_watch_logs.start_query(
        logGroupName=event_log_stream,
        startTime=query_start_date,
        endTime=query_end_date,
        queryString=query_string,
    )

    query_not_complete = True

    while query_not_complete:
        query_response = cloud_watch_logs.get_query_results(
            queryString=query_id,
        )
        if query_response['status'] == 'Complete':
            query_not_complete = False
    return query_response['results']
    

def add_month(query_response):
    amended_response = []
    for i in query_response['results']:
        amended_response.append(
            merge_two_dicts(
                query_response['results'][i],
                {'month': query_start_date},
            )    
        )
    return amended_response

def parse_results(query_results_1, query_results_2):
    object_with_month_2 = add_month(query_results_1)
    object_with_month_1 = add_month(query_results_2)
    combined_data = object_with_month_1 + object_with_month_2
    data_filename = 'sp_billing_data-%s.json' % (query_start_date)
    s3.put_object(
        Body=combined_data,
        Bucket=os.environ["QUICKSIGHT_BUCKET"],
        Key=data_filename,
    )

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
    

