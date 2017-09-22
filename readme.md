[![Build Status](https://travis-ci.org/TwylaHelps/twyla.logging.svg?branch=master)](https://travis-ci.org/TwylaHelps/twyla.logging)

Various logging utilities.

Sample dict config for the Loggly handler:

```
{
    'disable_existing_loggers': False,
    'handlers': {
        'loggly': {'class': 'twyla.logging.handlers.LogglyHTTPSHandler',
                   'level': 'INFO',
                   'tag': 'local',
                   'token': 'YOUR-TOKEN'}
    },
    'root': {'handlers': ['loggly'],
             'level': 'INFO'},
    'version': 1
}
```