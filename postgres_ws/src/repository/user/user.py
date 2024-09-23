import structlog

from sqlalchemy import (
    Engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    registry,
    sessionmaker,
    relationship
)

from sqlalchemy.dialects.postgresql import insert as pg_upsert

_USER_REPO_BASE = registry().generate_base()

'''
    NOTE:
    There are three relationship between data in database.
    1. one to one
        e.g. e-commerce => one member only have one shopping cart.
    2. one to many
        e.g. e-commerce => one category might include multiple products, but one product only inside one category.
    3. many to many
        e.g sports game => one sport game can provide thousands of audiences, and also one audience can attend multiple sport games.

    Primary key:
        A primary key is the column or colums that contains values that uniquely identify each row in a table
    Forigen key:
        A forigen key is a set of attributes in a table that refers to the primary key of another table, linking these two table.

    In database:
        we can use relationship function to generate relationship between two tables and we also can use join function.
'''


class User(_USER_REPO_BASE):
    __tablename__ = "users"  # table name in the databases

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)

    addresses = relationship('Address', uselist=True)


class Address(_USER_REPO_BASE):
    __tablename__ = "user_address"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)

    # Forigen Key => link address table and user table
    user_id = Column(Integer, ForeignKey("users.id"))


class UserRepo():

    def __init__(self,
                 logger: structlog.stdlib.BoundLogger,
                 engine: Engine):

        self.logger = logger

        # register engine/session_maker
        self.engine = engine
        self.session_maker = sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine)

    def register(self, user: User):

        with self.session_maker() as session:
            try:
                # do insert statement
                insert_stmt = pg_upsert(User).values({"id": user.id,
                                                      "name": user.name,
                                                      "username": user.username})

                # check conflict
                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=[User.id],
                    set_={"name": user.name,
                          "username": user.username})

                session.execute(do_update_stmt)
                session.commit()
            except Exception as e:
                session.rollback()
                self.logger.error(
                    "[UserRepo][register] register user failed. ERROR: {}".format(e))

    def register_address(self, address: Address):

        with self.session_maker() as session:
            try:
                # do insert statement
                insert_stmt = pg_upsert(Address).values({"id": address.id,
                                                         "address": address.address,
                                                         "user_id": address.user_id})

                # check conflict
                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=[Address.id],
                    set_={"address": address.address,
                          "user_id": address.user_id})

                session.execute(do_update_stmt)
                session.commit()
            except Exception as e:
                session.rollback()
                self.logger.error(
                    "[UserRepo][register] register user failed. ERROR: {}".format(e))

    def fetch_user_address(self) -> str:

        with self.session_maker() as session:
            try:
                user: User = session.query(User).first()
                for address in user.addresses:
                    self.logger.info("name: {}, user_name: {}, address: {}".format(
                        user.name, user.username, address.address))
            except Exception as e:
                session.rollback()
                self.logger.error(
                    "[UserRepo][fetch_user_address] fetch user address failed. ERROR: {}".format(e))


def setup_user_repo(logger: structlog.stdlib.BoundLogger, engine: Engine) -> UserRepo:

    _USER_REPO_BASE.metadata.create_all(engine)
    user_repo = UserRepo(logger=logger, engine=engine)
    return user_repo


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

    user_repo = setup_user_repo(
        logger=structlog.get_logger(), engine=pg_engine)

    user_repo.register(user=User(id=0, name="Chunwei", username="Andy"))
    user_repo.register_address(address=Address(
        id=0, address="New Taipei city", user_id=0))
    user_repo.register_address(address=Address(
        id=1, address="Taichung city", user_id=0))
    user_repo.fetch_user_address()
