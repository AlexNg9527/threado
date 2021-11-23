## Threado
A simple way to run multiple threads do the I/O

## Example
```python

import string
from threado.simple_thread_runner import SimpleThreadsRunner

actions = list(string.ascii_lowercase)
sr = SimpleThreadsRunner(5, lambda x:print("Thread output char:"+x))
sr.run_threads(iter_data=actions)

# In case the iter_data is large amounts of data
sr.run_threads(iter_data=actions, batch_size=20)

# Or it can be used separate as producer/consumer
for _ in actions:
    sr.q_producer(_)
    sr.q_consumer()
```


## Installing threado and Supported Versions

threado is available on PyPI:

```console
$ python -m pip install threado
```
