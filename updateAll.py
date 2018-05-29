import src.data.Market as Market
from datetime import datetime
import src.output.html_momenta as html_out

start_time = datetime.now()
print('Started at ' + str(start_time))

markets = ['XAMS', 'XBRU', 'XPAR']
momenta_dict = {}

for m in markets:
    print('Processing market: ' + m)
    market = Market.Market(m)
    # market.download_all_stock_data()
    momenta_dict[m] = market.momenta()

html_out.create_html_from_dict(momenta_dict)

end_time = datetime.now()
print('Finished at ' + str(end_time))
print('runtime: ' + str((end_time - start_time).total_seconds()) + 's')
