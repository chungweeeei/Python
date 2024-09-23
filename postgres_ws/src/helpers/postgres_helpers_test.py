import pytest
from assertpy import (
    assert_that, 
    fail
)

from config.settings import settings
from helpers import postgres_helpers

def test_pg_connectivity():

    try:
        postgres_helpers.connect_to_postgres(
            host=settings.host,
            port=settings.port,
            db_name=settings.db_name,
            user=settings.user,
            password=settings.password,
        )
    except Exception as e:
        fail(f"Error connecting to postgres: {str(e)}")