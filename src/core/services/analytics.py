import amplitude
import concurrent.futures



class Analytics:

	_instance = None
	
	def __init__(self, amplitude_api_token: str):

		if not hasattr(self, 'initialized'):

			self.client = amplitude.client.Amplitude(amplitude_api_token)
			self.executor = concurrent.futures.ThreadPoolExecutor(max_workers = 4)
			
			self.initialized = True

	def __new__(self, *args, **kwargs):

		if self._instance is None:

			self._instance = self.__init__(self, *args, **kwargs)

		return self._instance

	def send_event(self, user_id: str, event_type: str, event_properties: dict):

		pass

		