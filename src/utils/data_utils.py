import os
from typing import List
from urllib.request import urlretrieve
from zipfile import ZipFile

import pandas as pd

from src.utils.logging_utils import get_pylogger

log = get_pylogger(__name__)


def filter_dataframe_and_get_column(
    dataframe: pd.DataFrame, filter_column: str, filter_value: str, select_column: str
) -> List[str]:
    return dataframe[dataframe[filter_column] == filter_value][select_column].tolist()


def download_and_unzip(
    url: str, target_path: str, force_download: bool = False, remove_tmp_file: bool = False
):
    log.warning(f"download zip file from {url} to {target_path} ...")
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError(f"url needs to point to a http(s) address, but it is: {url}")
    tmp_file = os.path.join(target_path, os.path.basename(url))
    if os.path.exists(tmp_file) and not force_download:
        log.warning(f"tmp file {tmp_file} already exists, skip downloading {url}")
    else:
        urlretrieve(url, tmp_file)  # nosec
    with ZipFile(tmp_file, "r") as zfile:
        zfile.extractall(target_path)
    if remove_tmp_file:
        os.remove(tmp_file)
