# -*- coding: utf-8 -*-

"""
This script generate the IDP DB schema reference document from local dev db.
"""

import getpass
import sqlalchemy
from pathlib_mate import Path
from rstobj.directives import ListTable, CodeBlockSQL
from rstobj.markup import Header

username = getpass.getuser()
# by default, username is your $USER, and there's no password
conn_str = "postgresql+psycopg2://{}:@localhost:5432/upaya_development".format(username)
engine = sqlalchemy.create_engine(conn_str)
metadata = sqlalchemy.MetaData()
metadata.reflect(engine)

l = list()

for tname, t in sorted(metadata.tables.items(), key=lambda x: x[0]):
    title = "{table_name}".format(table_name=tname)
    h = Header(title=title, header_level=2)
    lt_data = [("name", "fullname", "type")]
    for cname, c in sorted(t.columns.items(), key=lambda x: x[0]):
        lt_data.append((
            CodeBlockSQL.from_string(cname),
            CodeBlockSQL.from_string(tname + "." + cname),
            str(c.type)
        ))
    lt = ListTable(data=lt_data, title="columns", index=False, header=True, class_="sortable")
    l.append(h)
    l.append(lt)
content = "\n\n".join([
    obj.render()
    for obj in l
])

p = Path(__file__).change(new_basename="IDP-DB-Schema.rst")
p.write_text(content, encoding="utf-8")
