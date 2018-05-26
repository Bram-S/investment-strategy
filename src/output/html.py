import pandas as pd
import settings
import time
import os


def create_html_momenta(code):
    momenta_path = os.path.join(settings.RESOURCES_ROOT, 'out', 'momenta' + '_' + code)
    csv_path = momenta_path + '.csv'
    last_edited_time = time.ctime(os.path.getmtime(csv_path))
    data = pd.read_csv(csv_path, index_col=0)
    value_format = {'Mean Volume': '{:,.2f}', 'Momentum': '{:.2%}'}
    caption = 'Market: ' + code + '\nLast updated: ' + last_edited_time
    html = data.style.format(value_format).set_caption(caption)

    with open(momenta_path + '.html', 'w') as file:
        file.write(html.render())


if __name__ == '__main__':
    create_html_momenta('XBRU')
