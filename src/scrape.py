# -*- coding: utf-8 -*-

from constants import EXECUTED_OFFENDERS_URL, ARCHIVE_HTML_FILENAME, DATAFRAME_FILENAME


from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import feather


def get_executed_offenders_html():
    response = requests.get(EXECUTED_OFFENDERS_URL)

    if response.status_code != 200:
        # TODO: account for non-OK responses
        pass

    return response.content


def get_executed_offenders_from_file(html_file=ARCHIVE_HTML_FILENAME):
    with open(html_file, 'r', encoding='latin-1') as fd:
        raw_html_content = fd.read()
    return raw_html_content


def get_executed_offenders_data():
    raw_html_content = get_executed_offenders_from_file()
    soup = BeautifulSoup(raw_html_content, 'html.parser')

    table = soup.find('table', {'class': 'os'})
    rows = table.findAll('tr')

    # data
    data_rows = rows[1:]

    # populate the data
    data = []
    for dr in data_rows:
        executed_offenders_data = dict()
        raw_row_data = dr.findAll('td')

        # execution number
        executed_offenders_data['execution_no'] = int(raw_row_data[0].text)

        # offender information link
        executed_offenders_data['offender_information_link'] = \
            raw_row_data[1].find('a', href=True).get('href')

        # last statement link
        executed_offenders_data['last_statement_link'] = \
            raw_row_data[2].find('a', href=True).get('href')

        # last name
        executed_offenders_data['last_name'] = raw_row_data[3].text
        # first name
        executed_offenders_data['first_name'] = raw_row_data[4].text

        # TDCJ number
        executed_offenders_data['tdcj_no'] = raw_row_data[5].text

        # age
        executed_offenders_data['age'] = int(raw_row_data[6].text)

        # date
        executed_offenders_data['date'] = datetime.strptime(
            raw_row_data[7].text, '%m/%d/%Y')

        # race
        executed_offenders_data['race'] = raw_row_data[8].text

        # county
        executed_offenders_data['county'] = raw_row_data[9].text

        data.append(executed_offenders_data)

    return data


def get_last_statements_data(eo_data):
    """
   `eo_data` stands for 'Executed Offenders Data'.
    """
    last_statements_data = []
    for eo in eo_data:
        last_statement_link = eo.get('last_statement_link')
        if last_statement_link is None:
            continue

        response = requests.get(last_statement_link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # extract body text
        body_text = [
            p.text.strip() for p in
            soup.find('div', {'id': 'body'}).findAll('p')
        ]

        # extract last statement
        last_statement = "\n".join(
            body_text[body_text.index('Last Statement:') + 1:]
        )

        last_statements_data.append(
            {
                'execution_no': eo['execution_no'],
                'last_statement': last_statement,
            }
        )

    return last_statements_data


def get_offender_information_data(eo_data):
    pass


def get_all_data():
    executed_offenders_data = get_executed_offenders_data()
    last_statements_data = get_last_statements_data(executed_offenders_data)

    return {
        'executed_offenders': executed_offenders_data,
        'last_statements': last_statements_data,
    }


def get_df(eo_data, ls_data):
    # executed offenders
    eo_df = pd.DataFrame(eo_data)
    # last statements
    ls_df = pd.DataFrame(ls_data)
    # merge and drop link columns
    df = pd.merge(eo_df, ls_df)
    df = df.drop('last_statement_link', 1)

    return df


def main():
    data = get_all_data()
    df = get_df(data['executed_offenders'], data['last_statements'])
    print(df)
    # save on disk
    feather.write_dataframe(df, DATAFRAME_FILENAME)


if __name__ == '__main__':
    main()
