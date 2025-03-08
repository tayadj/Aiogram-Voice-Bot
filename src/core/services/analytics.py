import amplitude
import concurrent.futures



class Analytics:
	
	def __init__(self, amplitude_api_token: str):

		self.client = amplitude.client.Amplitude(amplitude_api_token)
		self.executor = concurrent.futures.ThreadPoolExecutor(max_workers = 4)			

	def send_event(self, event_type: str, user_id: str, miscellaneous: dict = {}):

		event = amplitude.event.BaseEvent(
			event_type = event_type,
			event_properties = miscellaneous.get('event_properties', None),
			user_id = str(user_id),
			user_properties = miscellaneous.get('user_propreties', None),
			time = miscellaneous.get('time', None),
			region = miscellaneous.get('region', None),
			language = miscellaneous.get('language', None)
		)

		self.executor.submit(self.track_event, event)

	def track_event(self, event: amplitude.event.BaseEvent):

		self.client.track(event)
