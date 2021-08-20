from datetime import datetime
import json
import hashlib
import hmac
import base64
import requests
from typing import Optional
from az_custom_logging.utils.config import AuCustomLogConfig


#eda-au-nextgen
class AzCustomLogging:
	__projectId: str
	__config: object
	__customerId: str
	__sharedKey: str
	__logType: str
	__resource: str
	__logApi: str
	contentType: str = 'application/json'
	logMethod: str = 'POST'
	appName: str
	processId: str
	jobName: str

	def __init__(self, project_id: str, customer_id: str, shared_key: str, process_info: dict=None):
		self.__projectId = project_id
		self.__customerId = customer_id
		self.__sharedKey = shared_key	
		self.__config = AuCustomLogConfig.load_config(
			project_id=self.__projectId,
			customer_id=self.__customerId,
			shared_key=self.__sharedKey
		)
		self.__logType = self.__config.log_name
		self.__resource = self.__config.resource
		self.__logApi = self.__config.log_api_url

		if process_info and len(process_info):
			self.appName = process_info.get('app_name')
			self.processId = process_info.get('process_id')
			self.jobName = process_info.get('job_name')

	def log_info(self, message: str, **extra_args) -> bool:
		logRecord = self.__get_log_record(message=message, level=self.__config.info_label, **extra_args)
		return self.__log_record(record=logRecord)


	def log_error(self, message: str, **extra_args) -> bool:
		logRecord = self.__get_log_record(message=message, level=self.__config.error_label, **extra_args)
		return self.__log_record(record=logRecord)


	def log_debug(self, message: str, **extra_args) -> bool:
		logRecord = self.__get_log_record(message=message, level=self.__config.debug_label, **extra_args)
		return self.__log_record(record=logRecord)

	def __get_log_record(self, message: str, level: str, **process_args) -> dict:
		process_args = process_args or {}
		logRecord = {
			'level': level or self.__config.info_label,
			'app_name': process_args.get('app_name', self.appName),
			'process_id': process_args.get('process_id', self.processId),
			'job_name': process_args.get('job_name', self.jobName),
			'message': message
		}
		return logRecord

	def __get_headers(self, content_length: int) -> dict:		
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
		xHeaders = 'x-ms-date:' + date
		stringToHash = self.logMethod + '\n' + str(content_length) + '\n' + self.contentType + '\n' + xHeaders + '\n' + self.__resource
		bytesToHash = bytes(stringToHash, encoding='utf-8')
		decodedKey = base64.b64decode(self.__sharedKey)
		encodedHash = base64.b64encode(hmac.new(decodedKey, bytesToHash, digestmod=hashlib.sha256).digest()).decode()
		authorization = f'SharedKey {self.__customerId}:{encodedHash}'
		return authorization		


	def __log_record(self, record: dict) -> bool:
		logRecord = json.dumps(record)
		headers = self.__get_headers(content_length=len(logRecord))

		try:
			response = requests.post(self.__logApi, data=logRecord, headers=headers)

			if (response.status_code >= 200 and response.status_code <= 299):
				print('logged')
				return True
			else:
				#print(f'Response code: {response.status_code}')
				print(response.text)
				return False
		except Exception as err:
			pass

		return True

