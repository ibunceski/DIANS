from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import pandas as pd
from DataStorage import DataStorage


# indicator_factory.py
from abc import ABC, abstractmethod
from ta.momentum import (
    RSIIndicator, StochasticOscillator, WilliamsRIndicator,
    PercentagePriceOscillator, ROCIndicator
)
from ta.trend import (
    MACD, CCIIndicator, SMAIndicator, EMAIndicator,
    WMAIndicator, TRIXIndicator
)

class IndicatorFactory(ABC):
    @abstractmethod
    def create_indicator(self, data):
        pass

class OscillatorFactory(IndicatorFactory):
    def create_indicator(self, data):
        return {
            'RSI': RSIIndicator(close=data['Close'], window=14).rsi(),
            'Stoch_%K': StochasticOscillator(
                high=data['High'], low=data['Low'], close=data['Close'], window=14
            ).stoch(),
            'Stoch_%D': StochasticOscillator(
                high=data['High'], low=data['Low'], close=data['Close'], window=14
            ).stoch_signal(),
            'Williams_R': WilliamsRIndicator(
                high=data['High'], low=data['Low'], close=data['Close'], lbp=14
            ).williams_r(),
            'PPO': PercentagePriceOscillator(close=data['Close']).ppo(),
            'PPO_Signal': PercentagePriceOscillator(close=data['Close']).ppo_signal(),
            'ROC': ROCIndicator(close=data['Close'], window=12).roc(),
            'CCI': CCIIndicator(
                high=data['High'], low=data['Low'], close=data['Close'], window=20
            ).cci()
        }

class MovingAverageFactory(IndicatorFactory):
    def create_indicator(self, data):
        return {
            'SMA_20': SMAIndicator(close=data['Close'], window=20).sma_indicator(),
            'EMA_20': EMAIndicator(close=data['Close'], window=20).ema_indicator(),
            'WMA_20': WMAIndicator(close=data['Close'], window=20).wma(),
            'MACD': MACD(close=data['Close']).macd(),
            'MACD_Signal': MACD(close=data['Close']).macd_signal(),
            'TRIX': TRIXIndicator(close=data['Close'], window=20).trix()
        }

# signal_strategies.py
from abc import ABC, abstractmethod
import pandas as pd

class SignalStrategy(ABC):
    @abstractmethod
    def generate_signal(self, data, **kwargs):
        pass

class OscillatorSignalStrategy(SignalStrategy):
    def __init__(self, thresholds):
        self.thresholds = thresholds

    def generate_signal(self, value, indicator_name):
        if pd.isna(value):
            return 'Hold'

        thresholds = self.thresholds[indicator_name]
        if value <= thresholds['buy']:
            return 'Buy'
        elif value >= thresholds['sell']:
            return 'Sell'
        return 'Hold'

class MovingAverageSignalStrategy(SignalStrategy):
    def generate_signal(self, data, price_col, ma_col):
        signals = pd.Series('Hold', index=data.index)
        buffer = data[ma_col] * 0.01
        signals[data[price_col] > (data[ma_col] + buffer)] = 'Buy'
        signals[data[price_col] < (data[ma_col] - buffer)] = 'Sell'
        return signals

class MACDSignalStrategy(SignalStrategy):
    def generate_signal(self, row):
        macd = row['MACD']
        macd_signal = row['MACD_Signal']

        if pd.isna(macd) or pd.isna(macd_signal):
            return 'Hold'

        threshold = abs(macd_signal) * 0.15
        if macd > (macd_signal + threshold):
            return 'Buy'
        elif macd < (macd_signal - threshold):
            return 'Sell'
        return 'Hold'

# data_preprocessor.py
class DataPreprocessor:
    @staticmethod
    def preprocess_data(data):
        numeric_cols = [
            'Close', 'High', 'Low', 'Avg. Price', '%chg.',
            'Turnover in BEST in denars', 'Total turnover in denars', 'Volume'
        ]
        
        for col in numeric_cols:
            data[col] = (
                data[col]
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
                .astype(float)
            )

        data['Volume'] = data['Volume'].astype(int)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.sort_values('Date', ascending=True)
        data.set_index('Date', inplace=True)
        return data

# technical_analyzer.py
class TechnicalAnalyzer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TechnicalAnalyzer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.storage = DataStorage()
        self.thresholds = {
            'RSI': {'buy': 25, 'sell': 75},
            'Stoch_%K': {'buy': 15, 'sell': 85},
            'Williams_R': {'buy': -85, 'sell': -15},
            'PPO': {'buy': -1.5, 'sell': 1.5},
            'ROC': {'buy': -3, 'sell': 3},
            'CCI': {'buy': -150, 'sell': 150}
        }
        
        self.oscillator_factory = OscillatorFactory()
        self.ma_factory = MovingAverageFactory()
        self.oscillator_strategy = OscillatorSignalStrategy(self.thresholds)
        self.ma_strategy = MovingAverageSignalStrategy()
        self.macd_strategy = MACDSignalStrategy()
        self._initialized = True

    def generate_oscillator_signal(self, row, indicator_name):
        return self.oscillator_strategy.generate_signal(row[indicator_name], indicator_name)

    def generate_moving_average_signal(self, data, price_col, ma_col):
        return self.ma_strategy.generate_signal(data, price_col, ma_col)

    def generate_macd_signal(self, row):
        return self.macd_strategy.generate_signal(row)

    def preprocess_data(self, data):
        return DataPreprocessor.preprocess_data(data)

    def compute_indicators(self, data):
        oscillators = self.oscillator_factory.create_indicator(data)
        moving_averages = self.ma_factory.create_indicator(data)
        
        for indicator_name, values in oscillators.items():
            data[indicator_name] = values
            
        for indicator_name, values in moving_averages.items():
            data[indicator_name] = values
            
        return data

    def analyze_stock(self, issuer):
        db = self.storage.get_by_issuer(issuer)
        columns = [
            'Date', 'Issuer', 'Avg. Price', 'Close', 'High', 'Low', '%chg.',
            'Total turnover in denars', 'Turnover in BEST in denars', 'Volume'
        ]
        data = pd.DataFrame(db, columns=columns)

        data = self.preprocess_data(data)
        data = self.compute_indicators(data)

        oscillator_indicators = ['RSI', 'Stoch_%K', 'Williams_R', 'PPO', 'ROC', 'CCI']
        for indicator in oscillator_indicators:
            data[f'{indicator}_Signal'] = data.apply(
                self.generate_oscillator_signal, indicator_name=indicator, axis=1
            )

        ma_indicators = [('Close', 'SMA_20'), ('Close', 'EMA_20'),
                        ('Close', 'WMA_20'), ('Close', 'TRIX')]
        for price_col, ma_col in ma_indicators:
            data[f'{ma_col}_Signal'] = self.generate_moving_average_signal(data, price_col, ma_col)

        data['MACD_Signal'] = data.apply(self.generate_macd_signal, axis=1)

        data_weekly = data.resample('W').last()
        data_monthly = data.resample('ME').last()

        latest_daily_signal = data.iloc[-1].filter(like='_Signal')
        latest_weekly_signal = data_weekly.iloc[-1].filter(like='_Signal')
        latest_monthly_signal = data_monthly.iloc[-1].filter(like='_Signal')

        return {
            'daily': latest_daily_signal.to_dict(),
            'weekly': latest_weekly_signal.to_dict(),
            'monthly': latest_monthly_signal.to_dict()
        }