from dataclasses import dataclass

PROJECT_CONFIG = {
  'test-project': {
    'log_name': 'testCustomLog'
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
