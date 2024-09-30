import structlog

from config.settings import settings
from helpers.postgres_helpers import connect_to_postgres
from repository.robots.robots import (
    setup_robots_repo
)

from repository.user.user import (
    setup_user_repo
)

if __name__ == "__main__":

    pg_engine = connect_to_postgres(
        host=settings.host,
        port=settings.port,
        db_name=settings.db_name,
        user=settings.user,
        password=settings.password
    )

    LOGGER = structlog.get_logger()

    robots_repo = setup_robots_repo(logger=LOGGER, engine=pg_engine)
    user_repo = setup_user_repo(logger=LOGGER, engine=pg_engine)