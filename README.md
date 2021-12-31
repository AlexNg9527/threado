## Threado
A simple way to run multiple threads do the I/O

## Example
```python

import string
from threado.simple_thread_runner import SimpleThreadsRunner

actions = list(string.ascii_lowercase)
sr = SimpleThreadsRunner(5, lambda x:print("Thread output char:"+x))
sr.run_threads(iter_data=actions)

# In case the iter_data : Iterator[Any] is an Iterator of large amounts data

sr.run_threads(iter_data=actions, batch_size=20)

# Or it can be used separate as producer/consumer
for _ in actions:
    sr.q_producer(_)
    sr.q_consumer()

# File download
import urllib

url_list = [
    'https://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/dnd_text-150x93.png',
    'https://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/dnd_file-150x93.png',
    'https://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/panel_smack1-150x91.png'
]

def download_url(url: str):
    pic_name = url.split("/")[-1:][0]
    urllib.request.urlretrieve(url, pic_name)

sr = SimpleThreadsRunner(3, download_url)
sr.run_threads(iter_data=url_list)

# Simple load test
import time

def simple_loadTest(thread_count, func, load_test_data):
    sr = SimpleThreadsRunner(thread_count, func)
    index = 0
    for index, data in enumerate(load_test_data, start=1):
        sr.q_producer(data)

    _start = time.time()
    sr.q_consumer()
    _end = time.time()
    print(f"Total transitions: {index} \nTPS={index / (_end - _start)}")
```


## Installing threado and Supported Versions

threado is available on PyPI:

```console
$ python -m pip install threado
```
