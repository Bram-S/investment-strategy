import pandas as pd
import settings
import os


def create_html_momenta(code):
    momenta_path = os.path.join(settings.RESOURCES_ROOT, 'out', 'momenta' + '_' + code)
    data = pd.read_csv(momenta_path + '.csv', index_col=0)
    html = data.to_html()
    with open(momenta_path + '.html', 'w') as file:
        file.write(html)
