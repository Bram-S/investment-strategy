import src.data.Market as Market

markets = {'XAMS', 'XBUR', 'XPAR'}

for m in markets:
    market = Market(m)
    market.download_all_stock_data()
    market.momenta()
