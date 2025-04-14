from src.db.database import engine
from sqlalchemy import inspect

def check_schema():
    inspector = inspect(engine)
    print('Tables:', inspector.get_table_names())
    
    for table in inspector.get_table_names():
        print(f'\nTable: {table}')
        print('Columns:')
        for column in inspector.get_columns(table):
            print(f"  {column['name']}: {column['type']}")

if __name__ == "__main__":
    check_schema()
