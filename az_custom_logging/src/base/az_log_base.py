from abc import ABC, abstractmethod
from datetime import datetime
import json
import hashlib
import hmac
import base64
from typing import Optional
from az_custom_logging.src.utils.config import CustomLogConfig


class AzLogBase(ABC):

	__customerId: str
	__sharedKey: str
	__logType: str
	__processInfo: dict
	__config: object
	__resource: str
	__logApi: str
	contentType: str = 'application/json'
	logMethod: str = 'POST'
	apiTimeout: int = 120

	def __init__(self, customer_id: str, shared_key: str, log_name: str, process_info: dict):
		self.__customerId = customer_id
		self.__sharedKey = shared_key
		self.__logType = log_name
		self.__processInfo = process_info
		self.__config = CustomLogConfig.load_config(
			customer_id=self.__customerId,
			shared_key=self.__sharedKey,
			log_name=self.__logType
		)
		self.__resource = self.__config.resource
		self.__logApi = self.__config.log_api_url	

	@abstractmethod
	def log_info(self, message: str, **extra_args) -> bool:
		pass

	@abstractmethod
	def log_error(self, message: str, **extra_args) -> bool:
		pass

	@abstractmethod
	def log_debug(self, message: str, **extra_args) -> bool:
		pass

	def response_success(self, message: Optional[str] = None) -> dict:
		return {
			'status': 'success',
			'message': message
		}

	def response_error(self, message: str) -> dict:
		return {
			'status': 'error',
			'message': message
		}

	def __get_log_level(self, level: str) -> str:
		logLevel = {
			'info': self.__config.info_label,
			'error': self.__config.error_label,
			'debug': self.__config.debug_label
		}
		return logLevel.get(level)

	def __get_log_record(self, message: str, level: str, **process_args) -> dict:
		process_args = process_args or {}
		logRecord = {
			'level': self.__get_log_level(level=level),
			'message': message,
			**self.__processInfo,
			**process_args['extra_args']
		}
		if process_args and 'extra_args' in process_args:
			logRecord.update(dict(process_args['extra_args'].items()))
		return logRecord

	def __get_headers(self, content_length: int) -> dict:
		print(content_length)
		rfc1123Date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
		signature = self.__build_signature(date=rfc1123Date, content_length=content_length)
		headers = {
			'content-type': self.contentType,
			'Authorization': signature,
			'Log-Type': self.__logType,
			'x-ms-date': rfc1123Date,
			'time-generated-field': datetime.utcnow().isoformat()
		}
		return headers

	def __build_signature(self, date: str, content_length: int) -> str:
		print(content_length)
		xHeaders = 'x-ms-date:' + date
		stringToHash = self.logMethod + '\n' + str(content_length) + '\n' + self.contentType + '\n' + xHeaders + '\n' + self.__resource
		bytesToHash = bytes(stringToHash, encoding='utf-8')
		decodedKey = base64.b64decode(self.__sharedKey)
		encodedHash = base64.b64encode(hmac.new(decodedKey, bytesToHash, digestmod=hashlib.sha256).digest()).decode()
		authorization = f'SharedKey {self.__customerId}:{encodedHash}'
		return authorization

