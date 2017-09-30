# -*- coding: utf-8 -*-

import os

EXECUTED_OFFENDERS_URL = "http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html"

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(HERE)

_archive_dirname = "archive"
ARCHIVE_DIRNAME = os.path.join(BASE_DIR, _archive_dirname)

_html_filename = "DeathRowInformation_20170924.html"
ARCHIVE_HTML_FILENAME = os.path.join(
    ARCHIVE_DIRNAME, _html_filename
)

_data_dirname = "data"
DATA_DIRNAME = os.path.join(BASE_DIR, _data_dirname)

_dataframe_filename = "executed_offenders_last_statements.dat"
DATAFRAME_FILENAME = os.path.join(DATA_DIRNAME, _dataframe_filename)
