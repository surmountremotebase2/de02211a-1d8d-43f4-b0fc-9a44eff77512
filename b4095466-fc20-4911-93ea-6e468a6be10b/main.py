from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Define the meme stock ticker
        self.ticker = "AMC"
    
    @property
    def interval(self):
        # Use a 15-minute interval for intraday analysis
        return "15min"
    
    @property
    def assets(self):
        # The assets this strategy will trade
        return [self.ticker]
        
    def run(self, data):
        # Initialize the allocation with no position
        allocation_dict = {self.ticker: 0}
        
        # Calculate RSI and EMA for the meme stock
        rsi_values = RSI(self.ticker, data["ohlcv"], length=14)
        ema_short = EMA(self.ticker, data["ohlcv"], length=12)
        ema_long = EMA(self.ticker, data["ohlcv"], length=26)
        
        # Ensure we have enough data points to make a decision
        if rsi_values is not None and len(rsi_values) > 14 and len(ema_short) > 12 and len(ema_long) > 26:
            # Check if the stock is currently oversold and short-term EMA crosses above long-term EMA
            if rsi_values[-1] < 30 and ema_short[-1] > ema_long[-1]:
                log("Buying signal detected")
                allocation_dict[self.ticker] = 1  # Full allocation to AMC
            # Check if the stock is overbought or short-term EMA crosses below long-term EMA
            elif rsi_values[-1] > 70 or ema_short[-1] < ema_long[-1]:
                log("Selling signal detected")
                allocation_dict[self.ticker] = 0  # No allocation to AMC
        
        # Return the target allocation based on the defined logic


        return TargetAllocation(allocation_dict)