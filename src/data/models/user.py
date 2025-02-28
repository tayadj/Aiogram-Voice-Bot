import sqlalchemy
import sqlalchemy.orm



class ModelUser:

    class Base(sqlalchemy.orm.DeclarativeBase):

        pass

    class User(Base):

        __tablename__ = 'users'

        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
        value = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))
