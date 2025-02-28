import sqlalchemy



class ModelUser:

    class User(sqlalchemy.orm.declarative_base()):

        __tablename__ = 'users'

        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
        value = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String))

    # CRUD