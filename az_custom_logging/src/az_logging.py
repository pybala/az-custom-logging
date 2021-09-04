import json
import requests
from typing import Optional
from az_custom_logging.src.base.az_log_base import AzLogBase


class AzCustomLogging(AzLogBase):

	def log_info(self, message: str, **extra_args) -> bool:
		logRecord = self._AzLogBase__get_log_record(message=message, level='info', **extra_args)
		return self.__log_record(record=logRecord)

	def log_error(self, message: str, **extra_args) -> bool:
		logRecord = self._AzLogBase__get_log_record(message=message, level='error', **extra_args)
		return self.__log_record(record=logRecord)

	def log_debug(self, message: str, **extra_args) -> bool:
		logRecord = self._AzLogBase__get_log_record(message=message, level='debug', **extra_args)
		return self.__log_record(record=logRecord)
		
	def __log_record(self, record: dict) -> bool:
		logRecord = json.dumps(record).encode('utf-8')
		headers = self._AzLogBase__get_headers(content_length=len(logRecord))
		errorMsg = None
		
		try:
			response = requests.post(self._AzLogBase__logApi, data=logRecord, headers=headers, timeout=self.apiTimeout)
			if (response.status_code >= 200 and response.status_code <= 299):
				return self.response_success()
			else:
				errorMsg = str(response.text)
		except Exception as err:
			errorMsg = str(err)

		return self.response_error(message=errorMsg)
