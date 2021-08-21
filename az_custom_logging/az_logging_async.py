import json
import aiohttp
from az_custom_logging.az_logging import AzCustomLogging


class AzCustomLoggingAsync(AzCustomLogging):

	def __init__(self, project_id: str, customer_id: str, shared_key: str, process_info: dict=None):
		super().__init__(project_id=project_id, customer_id=customer_id, shared_key=shared_key, process_info=process_info)


	async def log_info(self, message: str, **extra_args) -> bool:
		logRecord = self._get_log_record(message=message, level=self._config.info_label, **extra_args)
		return await self._log_record(record=logRecord)


	async def log_error(self, message: str, **extra_args) -> bool:
		logRecord = self._get_log_record(message=message, level=self._config.error_label, **extra_args)
		return await self._log_record(record=logRecord)


	async def log_debug(self, message: str, **extra_args) -> bool:
		logRecord = self._get_log_record(message=message, level=self._config.debug_label, **extra_args)
		return await self._log_record(record=logRecord)	


	async def _log_record(self, record: dict) -> bool:
		logRecord = json.dumps(record).encode('utf-8')
		headers = self._get_headers(content_length=len(logRecord))

		try:
			async with aiohttp.ClientSession() as session:
				async with session.post(self._logApi, data=logRecord, headers=headers, timeout=120) as response:
					pass

			if 299 >= response.status >= 200:
				#print('logged')
				return True
			else:
				#print(await response.text())
				return False
		except Exception as err:
			pass

		return True

