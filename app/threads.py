import shutil
import requests
from io import StringIO
from os import path
from tempfile import NamedTemporaryFile
from tqdm import tqdm

from PySide6.QtCore import QThread, Signal


class DownloadThread(QThread):
    progress = Signal(int, str)

    def __init__(self, url: str, filename: str):
        super().__init__()
        self.url = url
        self.filename = filename

    def run(self):
        if not self.filename:
            self.filename = path.basename(self.url)

        request = requests.get(self.url, stream=True)

        total_size = int(request.headers.get("content-length", 0))
        scaling_factor = 100 / total_size
        block_size = 1024
        data = StringIO()
        progress = 0

        with NamedTemporaryFile(mode="wb", delete=False) as temp_file, tqdm(
            desc=path.basename(self.filename),
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
            file=data,
            bar_format="{desc}: {n_fmt}/{total_fmt} [{elapsed}/{remaining}, {rate_fmt}{postfix}]",
            leave=True,
        ) as progress_bar:
            for chunk in request.iter_content(chunk_size=block_size):
                temp_file.write(chunk)
                progress_bar.update(block_size)
                progress += block_size
                self.progress.emit(
                    progress * scaling_factor, data.getvalue().split("\r")[-1].strip()
                )

            temp_file.flush()
            temp_file.close()
        shutil.move(temp_file.name, self.filename)
