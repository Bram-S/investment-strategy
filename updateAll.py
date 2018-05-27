import src.data.Market as Market
import src.output.html_momenta as html_out

markets = ['XAMS', 'XBRU', 'XPAR']
momenta_dict = {}

for m in markets:
    market = Market.Market(m)
    print('Downloading ' + m)
    market.download_all_stock_data()
    momenta_dict[m] = market.momenta()

html_out.create_html_from_dict(momenta_dict)
