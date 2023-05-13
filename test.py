import sqlalchemy

someengine = sqlalchemy.create_engine("postgresql://dozer:simplepass@localhost/dozer")
backupengine = sqlalchemy.create_engine("sqlite://")

metadata_obj = sqlalchemy.MetaData()
metadata_obj.reflect(bind=someengine)

other_metadata = sqlalchemy.MetaData()

with backupengine.connect() as backup_connection:
    for table in reversed(metadata_obj.sorted_tables):
        table_obj = sqlalchemy.Table(table.name, other_metadata, autoload_with=backup_connection)
        table_obj.create(backup_connection)
        table_select = sqlalchemy.sql.expression.select(table.columns)
        table_as_connection = someengine.connect().execute(table_select)
        for row in table_as_connection:
            print(row)
            insert = sqlalchemy.sql.expression.insert(table).values(row)
            backup_connection.execute(insert)
