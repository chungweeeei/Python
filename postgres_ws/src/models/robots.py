import structlog
import itertools

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

    def fetch_robot_name(self, robot_ids: List[str]) -> Tuple:
        
        with self.session_maker() as session:
            
            try:
                robot_names: Row = session.query(RobotInfo.robot_name).filter(RobotInfo.robot_id.in_(robot_ids)).yield_per(10)
                # use itertools zip two list
                robot_names: List[str] = [row.robot_name for row in robot_names]
                robot_names = dict(zip(robot_ids, robot_names))
                self.logger.info(robot_names)
            except Exception as e:
                session.rollback()
                raise UnexpectedError(f"fetch robot_name failed. ERROR: {str(e)}")
            
    def fetch_robot_state(self):
        
        with self.session_maker() as session:
            
            try:
                '''
                    query multiple tables
                '''
                # query = session.query(RobotInfo, RobotState).join(RobotState, RobotInfo.robot_id == RobotState.robot_id).all()
                query = session.query(RobotInfo, RobotState).join(RobotState, RobotInfo.robot_id == RobotState.robot_id)
                results = query.yield_per(10)
                for robot_info, robot_state in results:
                    
                    self.logger.info("RobotInfo => robot_id: {}".format(robot_info.robot_id))
                    self.logger.info("RobotInfo => robot_name: {}".format(robot_info.robot_name))
                    
                    self.logger.info("RobotState => robot_id: {}".format(robot_state.robot_id))
                    self.logger.info("RobotState => map_uuid: {}".format(robot_state.map_uuid))
                    self.logger.info("RobotState => position_x: {}".format(robot_state.position_x))
                    self.logger.info("RobotState => position_y: {}".format(robot_state.position_y))
                    self.logger.info("RobotState => position_theta: {}".format(robot_state.position_theta))
            
            except Exception as e:
                session.rollback()
                raise UnexpectedError(f"fetch robot_state failed. ERROR: {str(e)}")

def setup_robots_repo(logger: structlog.stdlib.BoundLogger, engine: Engine) -> RobotsRepo:
    
    # create database table
    _ROBOTS_REPO_BASE.metadata.create_all(engine)
    
    robots_repo = RobotsRepo(logger=logger,
                             engine=engine)
    
    return robots_repo