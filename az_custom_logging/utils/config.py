from dataclasses import dataclass
from az_custom_logging.config.project_config import ProjectConfig

"""
Find a way to read customer_id and shared_key 
  for the respective project Log Analytics Workspace
"""


@dataclass(frozen=True)
class CustomLogConfig:
	project_id: str
	customer_id: str
	shared_key: str
	log_name: str
	resource:str = '/api/logs'
	api_version:str = '2016-04-01'
	log_api_url:str = None
	debug_label: str = 'DEBUG'
	info_label: str = 'INFO'
	error_label: str = 'ERROR'


	@staticmethod
	def load_config(project_id: str, customer_id: str, shared_key: str, log_name: str=None):
		projectConfig = ProjectConfig.load_config(project_id=project_id)
		resource = CustomLogConfig.resource
		apiVersion = CustomLogConfig.api_version
		apiUrl = f'https://{customer_id}.ods.opinsights.azure.com{resource}?api-version={apiVersion}'

		return CustomLogConfig(
			project_id=project_id,
			customer_id=customer_id,
			shared_key=shared_key,
			log_name=projectConfig.log_name,
			log_api_url=apiUrl
		)
