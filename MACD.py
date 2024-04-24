import pandas as pd
import matplotlib.pyplot as plt

def read_data(filename):
    data = pd.read_csv(filename)
    data = data.iloc[::-1].copy()
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y-%m-%d')
    data.reset_index(drop=True, inplace=True)
    return data

def ema(data):
    ema12 = data['close'].ewm(span=12, adjust=False).mean()
    ema26 = data['close'].ewm(span=26, adjust=False).mean()
    return ema12, ema26

def macd_calculation(ema12, ema26):
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def buy_sell(data, macd, signal):
    buy = []
    sell = []
    flag = -1
    for i in range(len(data['close'])):
        if macd[i] > signal[i]:
            sell.append(None)
            if flag != 1:
                buy.append(data['close'][i])
                flag = 1
            else:
                buy.append(None)
        elif macd[i] < signal[i]:
            buy.append(None)
            if flag != 0:
                sell.append(data['close'][i])
                flag = 0
            else:
                sell.append(None)
        else:
            buy.append(None)
            sell.append(None)
    return buy, sell

def macd_analysis(data, macd, signal):
    capital = 1000
    stock = 0
    buy, sell = buy_sell(data, macd, signal)
    for i in range(len(data['close'])):
        if buy[i] is not None:
            stock = capital / data['close'][i]
            capital = 0
        elif sell[i] is not None:
            capital = stock * data['close'][i]
            stock = 0
    if stock != 0:
        capital = stock * data['close'][i]
    print('Final capital: ', capital)

def defaultPlot(data, buy, sell):
    plt.figure(figsize=(10, 6))
    plt.plot(data['timestamp'], data['close'], linestyle='-')
    plt.scatter(data['timestamp'], buy, marker='^', color='green')
    plt.scatter(data['timestamp'], sell, marker='v', color='red')
    plt.title('Plot')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()


def macdPlot(data, macd, signal):
    plt.figure(figsize=(10, 6))
    plt.plot(data['timestamp'], macd, label='MACD', color='red')
    plt.plot(data['timestamp'], signal, label='Signal', color='blue')
    plt.legend(loc='upper left')
    plt.title('MACD and Signal')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()


filename = 'daily_NVDA.csv'

data = read_data(filename)
ema12, ema26 = ema(data)
macd, signal = macd_calculation(ema12, ema26)
buy, sell = buy_sell(data, macd, signal)
defaultPlot(data, buy, sell)
macdPlot(data, macd, signal)
macd_analysis(data, macd, signal)

data_last_200 = data[-200:]
macd_last_200 = macd[-200:]
signal_last_200 = signal[-200:]
buy_last_200 = buy[-200:]
sell_last_200 = sell[-200:]

defaultPlot(data_last_200, buy_last_200, sell_last_200)
macdPlot(data_last_200, macd_last_200, signal_last_200)
