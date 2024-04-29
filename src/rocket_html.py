import requests


class HtmlData:
    def __init__(self):
        self.url = "http://192.168.4.1/data"
        self.local_filename = "data.txt"
        self.html_filename = None

    def download_file(self, url, save_path):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        self
