import sqlalchemy
from sqlalchemy.ext.automap import automap_base

someengine = sqlalchemy.create_engine("postgresql://dozer:simplepass@localhost/dozer")
backupengine = sqlalchemy.create_engine("sqlite://")

metadata_obj = sqlalchemy.MetaData()
metadata_obj.reflect(bind=someengine)

Base = automap_base(metadata=metadata_obj)
Base.prepare()

with backupengine.connect() as backup_connection:
    for table in Base.classes:
        print(dir(table))
        table_obj = sqlalchemy.Table(table.name, Base.metadata, schema=table.schema)
        print(table_obj.dialect_options)
        table_obj.create(backup_connection)
        table_select = sqlalchemy.sql.expression.select(table.columns)
        table_as_connection = someengine.connect().execute(table_select)
        for row in table_as_connection:
            print(row)
            insert = sqlalchemy.sql.expression.insert(table).values(row)
            backup_connection.execute(insert)
