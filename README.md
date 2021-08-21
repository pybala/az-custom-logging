# Azure Custom Logging using Data collector - Python

Define your project custom log name in project_config.py and use it as project_id to initiate the logging.
Added support for async as well.

### How to

```python
from az_custom_logging import AzCustomLogging

processInfo = {
  'process_id': '<uuid>',
  'app_name': 'test-app-1',
  'job_name': 'test-job-1'
}
cl = AzCustomLogging(
  project_id='test-project',
  customer_id='<Customer Id from Log Analytics Worksapce>',
  shared_key='<Shared key from Log Analytics Worksapce>',
  process_info=processInfo
)

cl.log_info(message='test info log')
```

### How to - Async

```python
import asyncio
from az_custom_logging import AzCustomLoggingAsync

processInfo = {
  'process_id': '<uuid>',
  'app_name': 'test-app-1',
  'job_name': 'test-job-1'
}
cl = AzCustomLoggingAsync(
  project_id='test-project',
  customer_id='<Customer Id from Log Analytics Worksapce>',
  shared_key='<Shared key from Log Analytics Worksapce>',
  process_info=processInfo
)

#loop = asyncio.get_event_loop()
#loop.run_until_complete(cl.log_info(message='test info log 1'))

asyncio.run(cl.log_error(message='test info log 2'))
```

## Sample logs from my Custom log space

![](./custom-log-example.png)
