import pandas as pd
import settings
import time
from datetime import datetime
import os
from bs4 import BeautifulSoup


def create_html_from_csv(code):
    momenta_path = os.path.join(settings.RESOURCES_ROOT, 'out', 'momenta' + '_' + code)
    csv_path = momenta_path + '.csv'
    last_edited_time = time.ctime(os.path.getmtime(csv_path))
    momenta = pd.read_csv(csv_path, index_col=0)
    html = _momemta_to_html_table(momenta, code, last_edited_time)
    soup = BeautifulSoup(html, 'lxml')

    with open(momenta_path + '.html', 'w') as file:
        file.write(soup.prettify())


def create_html_from_dict(momenta_dict):
    html = ""
    last_edited_time = str(datetime.now())
    momenta_path = os.path.join(settings.RESOURCES_ROOT, 'out', 'all_momenta')

    for code, momenta in momenta_dict.items():
        html += _momemta_to_html_table(momenta, code, last_edited_time)

    soup = BeautifulSoup(html, 'lxml')

    with open(momenta_path + '.html', 'w') as file:
        file.write(soup.prettify())


def _momemta_to_html_table(momenta, code, last_edited_time):
    value_format = {'Mean Volume': '{:,.2f}', 'Momentum': '{:.2%}'}
    caption = 'Market: ' + code + '\nLast updated: ' + last_edited_time

    return momenta.style.format(value_format).set_caption(caption).render()


if __name__ == '__main__':
    create_html_from_csv('XBRU')
