import sqlalchemy

someengine = sqlalchemy.create_engine("postgresql://dozer:simplepass@localhost/dozer")
backupengine = sqlalchemy.create_engine("sqlite://")

metadata_obj = sqlalchemy.MetaData()
metadata_obj.reflect(bind=someengine)
metadata_obj.create_all(backupengine, checkfirst=True)
with backupengine.connect() as backup_connection:
    for table in reversed(metadata_obj.sorted_tables):
        table_select = sqlalchemy.sql.expression.select(table.columns)
        table_as_connection = someengine.connect().execute(table_select)
        # table.create(backup_connection)
        for row in table_as_connection:
            print(row)
            insert = sqlalchemy.sql.expression.insert(table).values(row)
            backup_connection.execute(insert)
