import structlog

from config.settings import settings
from helpers.postgres_helpers import connect_to_postgres
from repository.robots.robots import (
    RobotInfo,
    RobotState,
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

    robots_repo = setup_robots_repo(
        logger=structlog.get_logger(), engine=pg_engine)

    setup_user_repo(logger=structlog.get_logger(), engine=pg_engine)

    # robots_repo.register([RobotInfo(robot_id="smr01", robot_name="01"),
    #                       RobotInfo(robot_id="smr02", robot_name="02"),
    #                       RobotInfo(robot_id="smr03", robot_name="03"),
    #                       RobotInfo(robot_id="smr04", robot_name="04"),
    #                       RobotInfo(robot_id="smr05", robot_name="05")])

    # robots_repo.upsert_robot_states([RobotState(robot_id="smr01",
    #                                             map_uuid="xxx",
    #                                             position_x=0.0,
    #                                             position_y=0.0,
    #                                             position_theta=0.0)])

    # robots_repo.fetch_robot_name(robot_ids=["smr01", "smr02"])

    # robots_repo.fetch_robot_state()
