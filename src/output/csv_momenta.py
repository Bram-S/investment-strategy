import os
import settings


def csv(momenta, code):
    momenta_path = os.path.join(settings.RESOURCES_ROOT, 'out', 'momenta' + '_' + code + '.csv')
    momenta.to_csv(momenta_path)
