import numpy as np

def calculate_metrics(nav_history: list, trades: list, risk_free_rate_annual: float = 0.06):
    """
    Calculate performance metrics based on NAV history and trades log.
    
    Args:
        nav_history: list of float, daily Net Asset Value
        trades: list of dict, trade logs containing {'action', 'profit_loss'} for SELL trades
        risk_free_rate_annual: float, annual risk-free rate (default 6%)
        
    Returns:
        dict: Performance metrics
    """
    if not nav_history or len(nav_history) < 2:
        return {
            "Cumulative Return": 0.0,
            "Sharpe Ratio": 0.0,
            "Max Drawdown": 0.0,
            "Win Rate": 0.0
        }
        
    # 1. Cumulative Return
    initial_nav = nav_history[0]
    final_nav = nav_history[-1]
    cumulative_return = (final_nav - initial_nav) / initial_nav
    
    # 2. Sharpe Ratio
    # Convert NAV history to daily returns
    daily_returns = np.diff(nav_history) / nav_history[:-1]
    
    # Daily risk-free rate (approx 252 trading days)
    daily_rf = risk_free_rate_annual / 252.0
    
    # Excess returns
    excess_returns = daily_returns - daily_rf
    
    if len(excess_returns) > 0 and np.std(excess_returns) > 0:
        # Annualized Sharpe Ratio
        sharpe_ratio = np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)
    else:
        sharpe_ratio = 0.0
        
    # 3. Maximum Drawdown
    nav_array = np.array(nav_history)
    peak = np.maximum.accumulate(nav_array)
    drawdown = (nav_array - peak) / peak
    max_drawdown = np.min(drawdown)
    
    # 4. Win Rate
    # A trade is considered a "Win" if we sold for a profit. 
    # Trades list is expected to track realized profit_loss on SELL actions.
    sell_trades = [t for t in trades if t.get('action') == 'SELL' and 'profit_loss' in t]
    
    if sell_trades:
        winning_trades = len([t for t in sell_trades if t['profit_loss'] > 0])
        win_rate = winning_trades / len(sell_trades)
    else:
        win_rate = 0.0
        
    return {
        "Cumulative Return": cumulative_return,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown,
        "Win Rate": win_rate
    }
