import src.data.Market as Market

markets = {'XAMS', 'XBRU', 'XPAR'}

for m in markets:
    market = Market.Market(m)
    market.download_all_stock_data()
    market.momenta()
