from sqlalchemy import (
    Engine, 
    text,
    create_engine, 
)
from sqlalchemy.orm import Session

from sqlalchemy_utils import (
    create_database, 
    database_exists, 
    drop_database
)


def _execute(engine: Engine, sql: str, raise_error: bool = True):

    with engine.connect() as conn:
        try:
            conn.execute(text(sql))
            conn.commit()
        except Exception as e:
            if 'psycopg2.errors.DuplicateColumn' in str(e):
                # print(
                #     f"Column already exists in table. Skipping addition. {repr(e)}")
                return

            if raise_error:
                raise e
            # print(">>> ", repr(e))


def connect_to_postgres(
    host: str,
    port: int,
    db_name: str = "test_db",
    user="root",
    password="root"
):

    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{db_name}",
        pool_size=10
    )
    
    if not database_exists(engine.url):
        create_database(engine.url)
    
    _execute(engine, f"ALTER DATABASE \"{db_name}\" SET timezone TO 'Asia/Taipei';")
    
    return engine