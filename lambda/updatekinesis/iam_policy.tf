data "aws_iam_policy_document" "assume_role" {
    statement {
        sid = "AssumeRole"
        actions = ["sts:AssumeRole"]

        principals {
            type        = "Service"
            identifiers = ["lambda.amazonaws.com"]
        }
    }
}

resource "aws_iam_role" "kinesis" {
    name = "${var.env_name}-lambda_update_kinesis"
    path = "/"
    assume_role_policy = "${data.aws_iam_policy_document.assume_role.json}"
 }

data "aws_iam_policy_document" "cloudwatch_access" {
    statement {
        sid = "CloudWatch"
        effect = "Allow"
        actions = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ]
        resources = [
            "*"
        ]
    }
}

resource "aws_iam_role_policy_attachment" "cloudwatch_access" {
    role       = "${aws_iam_role.kinesis.name}"
    policy_arn = "${aws_iam_policy.cloudwatch_access.arn}"
}

data "aws_iam_policy_document" "firehose" {
    statement {
        sid = "firehose"
        effect = "Allow"
        actions = [
            "firehose:UpdateDestination"
        ]
        resources = [
            "arn:aws:firehose:us-east-1:540430061122:deliverystream/test1"
        ]
    }

    statement {
        sid = "firehose"
        effect = "Allow"
        actions = [
            "firehose:DescribeDeliveryStream"
        ]
        resources = [
            "*"
        ]
    }
}

resource "aws_iam_role_policy_attachment" "firehose" {
    role       = "${aws_iam_role.kinesis.name}"
    policy_arn = "${aws_iam_policy.firehose.arn}"
}

data "aws_iam_policy_document" "secretsmanager" {
    statement {
        sid = "secretsmanager"
        effect = "Allow"
        actions = [
            "secretsmanager:GetSecretValue"
        ]
        resources = [
            "aarn:aws:secretsmanager:us-east-1:540430061122:secret:dev/*"
        ]
    }
}

resource "aws_iam_role_policy_attachment" "secretsmanager" {
    role       = "${aws_iam_role.kinesis.name}"
    policy_arn = "${aws_iam_policy.secretsmanager.arn}"
}
