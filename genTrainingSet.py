#SKnight 2021 MIT

def getTrainingSet(totalBank, timerange, strategy, configuration,  hyperopt, hyperoptLoss, epoch, timeframe):
    backtesting = "freqtrade backtesting --config %s.json -s %s --timerange=%s --dry-run-wallet %s --timeframe %s"%(configuration,strategy,timerange,totalBank, timeframe)
    hyperoptimization = "freqtrade hyperopt --hyperopt %s --hyperopt-loss %s --spaces roi stoploss trailing --strategy %s --config %s.json -e %s --timerange=%s --dry-run-wallet %s --timeframe %s"%(hyperopt,hyperoptLoss,strategy,configuration,epoch,timerange,totalBank, timeframe)
    data = "freqtrade download-data --config %s.json --timeframe %s --days 1 --dl-trades"%(configuration, timeframe)
    trade = "freqtrade trade --config %s.json -s %s --dry-run-wallet %s"%(configuration,strategy, totalBank)
    print(backtesting)
    print(hyperoptimization)
    print(data)
    print(trade)
timeframes = ['5m','15m','1h','12h', '1d']
for time in timeframes:
    print(time)
    #getTrainingSet('0.2', '20210101-', 'HeraclesDOGEBTCBULL', 'configDOGEBTC', 'HeraclesHo', 'SharpeHyperOptLossDaily', '100', time)
    #getTrainingSet('0.2', '20210101-', 'Heracles', 'configDOGEBTC', 'HeraclesHo', 'SharpeHyperOptLossDaily', '100', time)
    #getTrainingSet('2.5', '20210319-20210401', 'Quickie', 'configAltEth', 'mabStraHo', 'SharpeHyperOptLossDaily', '100', time)
    #getTrainingSet('2.5', '20210322-20210410', 'BbandRsi', 'configAltEth2Bull', 'HeraclesHo', 'SharpeHyperOptLossDaily', '100', time)
    #getTrainingSet('2000', '20191219-', 'plasma_cutter', 'configETHUSDT', 'mabStraHo', 'SharpeHyperOptLossDaily', '100', time)
    getTrainingSet('200', '20191219-', 'Heracles', 'configBTCUSDT', 'HeraclesHo', 'SharpeHyperOptLossDaily', '100', time)

#freqtrade convert-trade-data --format-from jsongz --format-to json --datadir ~/.freqtrade/data/kraken --erase
