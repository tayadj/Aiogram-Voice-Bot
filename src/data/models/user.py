import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.future
import sqlalchemy.orm



class ModelUser:

    class Base(sqlalchemy.orm.DeclarativeBase):

        pass

    class User(Base):

        __tablename__ = 'users'

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(sqlalchemy.BigInteger, primary_key = True)
        values: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column()

    async def create_user(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int, values: str):

        user = self.User(id = id, values = values)
        database.add(user)

        await database.commit()
        await database.refresh(user)

        return user

    async def read_user(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int):

        user = await database.get(self.User, id)

        return user

    async def update_user(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int, values: str):

        user = await database.get(self.User, id)
        user.values = values

        await database.commit()
        await database.refresh(user)

        return user

    async def delete_user(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int):

        user = await database.get(self.User, id)

        await database.delete(user)
        await database.commit()

        return user