from .models import ModelUser

import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.orm



class Database:

	def __init__(self, url):


		#AsyncAdaptedPool!!!
		self.url = url
		self.engine = sqlalchemy.ext.asyncio.create_async_engine(
			self.url, 
			echo = True
		)
		self.session_local = sqlalchemy.orm.sessionmaker(
			bind = self.engine, 
			class_ = sqlalchemy.ext.asyncio.AsyncSession, 
			expire_on_commit = False
		)

		self.model_user = ModelUser()
