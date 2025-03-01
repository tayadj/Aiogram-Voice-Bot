import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.orm



class ModelUser:

    class Base(sqlalchemy.orm.DeclarativeBase):

        pass

    class User(Base):

        __tablename__ = 'users'

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key = True)
        user: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(unique = True)
        value: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column()

    async def create_user(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int, user: int, value: str):

        user = self.User(id = id, user = user, value = value)
        database.add(user)
        await database.commit()
        await database.refresh(user)
