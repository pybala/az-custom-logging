from datetime import datetime
import json
import hashlib
import hmac
import base64
import requests
from typing import Optional
from az_custom_logging.src.utils.config import CustomLogConfig


class AzCustomLogging:
	__customerId: str
	__sharedKey: str
	__logName: str
	__logType: str
	__resource: str
	_config: object
	_logApi: str
	contentType: str = 'application/json'
	logMethod: str = 'POST'
	__processInfo: dict
	processId: str
	jobName: str

	def __init__(self, customer_id: str, shared_key: str, log_name: str, process_info: dict):
		"""
		ToDo: Validation for log_name
			  process_info => restrict to defined properties
			  	- must fields: process_id, job_name
		"""
		self.__customerId = customer_id
		self.__sharedKey = shared_key
		self.__logType = log_name
		self._config = CustomLogConfig.load_config(
			customer_id=self.__customerId,
			shared_key=self.__sharedKey,
			log_name=self.__logType
		)
		#self.__logType = self._config.log_name
		self.__resource = self._config.resource
		self._logApi = self._config.log_api_url
		self.__processInfo = process_info

		if process_info and len(process_info):
			self.processId = process_info.get('process_id')
			self.jobName = process_info.get('job_name')

	def log_info(self, message: str, **extra_args) -> bool:
		logRecord = self._get_log_record(message=message, level=self._config.info_label, **extra_args)
		return self._log_record(record=logRecord)

	def log_error(self, message: str, **extra_args) -> bool:
		logRecord = self._get_log_record(message=message, level=self._config.error_label, **extra_args)
		return self._log_record(record=logRecord)

	def log_debug(self, message: str, **extra_args) -> bool:
		logRecord = self._get_log_record(message=message, level=self._config.debug_label, **extra_args)
		return self._log_record(record=logRecord)

	def _get_log_record(self, message: str, level: str, **process_args) -> dict:
		process_args = process_args or {}
		logRecord = {
			'level': level or self._config.info_label,
			'message': message,
			**self.__processInfo,
			**process_args
		}
		return logRecord

	def _get_headers(self, content_length: int) -> dict:		
		rfc1123Date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
		signature = self._build_signature(date=rfc1123Date, content_length=content_length)
		headers = {
			'content-type': self.contentType,
			'Authorization': signature,
			'Log-Type': self.__logType,
			'x-ms-date': rfc1123Date,
			'time-generated-field': datetime.utcnow().isoformat()
		}
		return headers


	def _build_signature(self, date: str, content_length: int) -> str:
		xHeaders = 'x-ms-date:' + date
		stringToHash = self.logMethod + '\n' + str(content_length) + '\n' + self.contentType + '\n' + xHeaders + '\n' + self.__resource
		bytesToHash = bytes(stringToHash, encoding='utf-8')
		decodedKey = base64.b64decode(self.__sharedKey)
		encodedHash = base64.b64encode(hmac.new(decodedKey, bytesToHash, digestmod=hashlib.sha256).digest()).decode()
		authorization = f'SharedKey {self.__customerId}:{encodedHash}'
		return authorization		


	def _log_record(self, record: dict) -> bool:
		logRecord = json.dumps(record).encode('utf-8')
		headers = self._get_headers(content_length=len(logRecord))

		try:
			response = requests.post(self._logApi, data=logRecord, headers=headers, timeout=120)

			if (response.status_code >= 200 and response.status_code <= 299):
				#print('logged')
				return True
			else:
				#print(response.text)
				return False
		except Exception as err:
			pass

		return True

