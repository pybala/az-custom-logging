from dataclasses import dataclass

"""
Not used
"""

PROJECT_CONFIG = {
	'test-project': {
		'log_name': 'poc_custom_logging'
	}
}

@dataclass(frozen=True)
class ProjectConfig:
	project_id: str
	log_name: str

	@staticmethod
	def load_config(project_id: str, log_name: str=None):
		projectConfig = PROJECT_CONFIG[project_id]
		logName = projectConfig['log_name']

		return ProjectConfig(
			project_id=project_id,
			log_name=logName
		)
