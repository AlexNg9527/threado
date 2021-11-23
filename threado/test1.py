import urllib.request
from threado.simple_thread_runner import SimpleThreadsRunner

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
