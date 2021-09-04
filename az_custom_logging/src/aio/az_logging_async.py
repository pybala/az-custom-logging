import json
import aiohttp
from az_custom_logging.src.base.az_log_base import AzLogBase


class AzCustomLoggingAsync(AzLogBase):

	async def log_info(self, message: str, **extra_args) -> bool:
		logRecord = self._AzLogBase__get_log_record(message=message, level='info', **extra_args)
		return await self.__log_record(record=logRecord)

	async def log_error(self, message: str, **extra_args) -> bool:
		logRecord = self._AzLogBase__get_log_record(message=message, level='error', **extra_args)
		return await self.__log_record(record=logRecord)

	async def log_debug(self, message: str, **extra_args) -> bool:
		logRecord = self._AzLogBase__get_log_record(message=message, level='debug', **extra_args)
		return await self.__log_record(record=logRecord)

	async def __log_record(self, record: dict) -> bool:
		logRecord = json.dumps(record).encode('utf-8')
		headers = self._AzLogBase__get_headers(content_length=len(logRecord))
		errorMsg = None

		try:
			async with aiohttp.ClientSession() as session:
				async with session.post(self._AzLogBase__logApi, data=logRecord, headers=headers, timeout=self.apiTimeout) as response:
					#resp = await response.text()
					#print(resp)
					if 299 >= response.status >= 200:
						return self.response_success()
					else:
						errorMsg = str(await response.text())
		except Exception as err:
			errorMsg = str(err)

		return self.response_error(message=errorMsg)

