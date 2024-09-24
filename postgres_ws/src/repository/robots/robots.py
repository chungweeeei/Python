import structlog

from pydantic import (
    BaseModel,
    Field
)

from typing import (
    List,
    Dict,
    Tuple
)

from sqlalchemy import (
    Engine,
    Column,
    String,
    Float
)

from sqlalchemy.orm import (
    registry, 
    sessionmaker
)

from sqlalchemy.engine.row import Row

from sqlalchemy.dialects.postgresql import insert 

_ROBOTS_REPO_BASE = registry().generate_base()

'''
    NOTE:
    A JOIN clause is used to combine rows from two or more tables,
    based on a related column between him.
'''

class UnexpectedError(Exception):
    pass

class RobotInfo(_ROBOTS_REPO_BASE):
    __tablename__ = "robot_infos"
    robot_id = Column(String, primary_key=True)
    robot_name = Column(String)

class RobotState(_ROBOTS_REPO_BASE):
    __tablename__ = "robot_states"
    robot_id = Column(String, primary_key=True)
    map_uuid = Column(String)
    position_x = Column(Float)
    position_y = Column(Float)
    position_theta = Column(Float)

class LatestRobotState(BaseModel):
    robot_id: str = Field(..., example="smr01", description="robot serial number")
    robot_name: str = Field(..., example="01", description="custom defined name of robot")
    map_uuid: str = Field(..., example="123", description="map")
    position_x: float = Field(..., example=0.0, description="current robot x position")
    position_y: float = Field(..., example=0.0, description="current robot y position")
    position_theta: float = Field(..., example=0.0, description="current robot theta position")

class RobotsRepo():
    
    def __init__(self, 
                 logger: structlog.stdlib.BoundLogger,
                 engine: Engine):
        
        # register logger handler
        self.logger = logger
        
        # register engine
        self.engine = engine
        self.session_maker = sessionmaker(autocommit=False, 
                                          autoflush=False, 
                                          bind=engine)

    def register(self, robot_infos: List[RobotInfo]):
        
        with self.session_maker() as session:
            try:
                insert_stmt = insert(RobotInfo).values(
                    [{
                        "robot_id": robot_info.robot_id,
                        "robot_name": robot_info.robot_name,
                    } for robot_info in robot_infos])

                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=[RobotInfo.robot_id],
                    set_={"robot_name": insert_stmt.excluded.robot_name})
    
                session.execute(do_update_stmt)
                session.commit()
            except Exception as e:
                session.rollback()
                raise UnexpectedError(f"register robot infos failed. ERROR: {str(e)}")

    def upsert_robot_states(self, robot_states: RobotState):
        
        with self.session_maker() as session:
            
            try:
                insert_stmt = insert(RobotState).values(
                    [{
                        "robot_id": robot_state.robot_id,
                        "map_uuid": robot_state.map_uuid,
                        "position_x": robot_state.position_x,
                        "position_y": robot_state.position_y,
                        "position_theta": robot_state.position_theta,
                    } for robot_state in robot_states])

                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=[RobotState.robot_id],
                    set_={"map_uuid": insert_stmt.excluded.map_uuid,
                          "position_x": insert_stmt.excluded.position_x,
                          "position_y": insert_stmt.excluded.position_y,
                          "position_theta": insert_stmt.excluded.position_theta})
    
                session.execute(do_update_stmt)
                session.commit()
            except Exception as e:
                session.rollback()
                raise UnexpectedError(f"update robot states failed. ERROR: {str(e)}")

    def fetch_robot_states(self) -> List[LatestRobotState]:
        
        robot_states = []
        with self.session_maker() as session:
            
            try:
                '''
                    query multiple tables
                '''
                # query = session.query(RobotInfo, RobotState).join(RobotState, RobotInfo.robot_id == RobotState.robot_id).all()
                query = session.query(RobotInfo, RobotState).join(RobotState, RobotInfo.robot_id == RobotState.robot_id)
                results = query.yield_per(10)
                robot_states = [LatestRobotState(robot_id=robot_info.robot_id,
                                                 robot_name=robot_info.robot_name,
                                                 map_uuid=robot_state.map_uuid,
                                                 position_x=robot_state.position_x,
                                                 position_y=robot_state.position_y,
                                                 position_theta=robot_state.position_theta) for robot_info, robot_state in results]
            except Exception as e:
                session.rollback()
                raise UnexpectedError(f"fetch robot_state failed. ERROR: {str(e)}")

        return robot_states

    def fetch_robot_name(self, robot_ids: List[str]) -> List:
        
        robot_names = []
        with self.session_maker() as session:
            
            try:
                '''
                    NOTE:
                    in sqlalchemy, we can use in_ function filter table by a list
                '''
                robot_names: Row = session.query(RobotInfo.robot_name).filter(RobotInfo.robot_id.in_(robot_ids)).yield_per(10)
                
                # use zip two list
                robot_names: List[str] = [row.robot_name for row in robot_names]
                # robot_names = dict(zip(robot_ids, robot_names))
            except Exception as e:
                session.rollback()
                raise UnexpectedError(f"fetch robot_name failed. ERROR: {str(e)}")
        
        return robot_names


def setup_robots_repo(logger: structlog.stdlib.BoundLogger, engine: Engine) -> RobotsRepo:
    
    # create database table
    _ROBOTS_REPO_BASE.metadata.create_all(engine)
    
    robots_repo = RobotsRepo(logger=logger,
                             engine=engine)
    
    return robots_repo

if __name__ == "__main__":
    
    # register db_engine
    from helpers.postgres_helpers import connect_to_postgres
    from config.settings import settings

    pg_engine = connect_to_postgres(
        host=settings.host,
        port=settings.port,
        db_name=settings.db_name,
        user=settings.user,
        password=settings.password
    )
    
    robots_repo = setup_robots_repo(logger=structlog.get_logger(), engine=pg_engine)

    robots_repo.register([RobotInfo(robot_id="smr01", robot_name="01"),
                          RobotInfo(robot_id="smr02", robot_name="02"),
                          RobotInfo(robot_id="smr03", robot_name="03"),
                          RobotInfo(robot_id="smr04", robot_name="04"),
                          RobotInfo(robot_id="smr05", robot_name="05")])

    robots_repo.upsert_robot_states([RobotState(robot_id="smr01",
                                                map_uuid="xxx",
                                                position_x=0.0,
                                                position_y=0.0,
                                                position_theta=0.0)])

    robot_names = robots_repo.fetch_robot_name(robot_ids=["smr01", "smr02"])
    structlog.get_logger().info(robot_names)

    robot_states = robots_repo.fetch_robot_states()
    structlog.get_logger().info(robot_states)