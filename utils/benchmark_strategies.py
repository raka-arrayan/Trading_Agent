import pandas as pd
import numpy as np

def run_buy_and_hold(df: pd.DataFrame, initial_capital: float = 100000000.0, fee_rate: float = 0.002) -> pd.DataFrame:
    """Strategi pasif: Beli di hari pertama, tahan sampai akhir."""
    result_df = df.copy()
    
    # Beli sedapatnya di hari pertama
    first_price = result_df['close'].iloc[0]
    shares_bought = (initial_capital * (1 - fee_rate)) // first_price
    cash = initial_capital - (shares_bought * first_price * (1 + fee_rate))
    
    result_df['portfolio_value'] = (result_df['close'] * shares_bought) + cash
    result_df['strategy'] = 'Buy & Hold'
    return result_df

def run_sma_crossover(df: pd.DataFrame, initial_capital: float = 100000000.0, fee_rate: float = 0.002) -> pd.DataFrame:
    """Strategi aktif: Beli jika SMA-20 memotong ke atas SMA-50 (Golden Cross), Jual jika ke bawah (Death Cross)."""
    result_df = df.copy()
    
    # Asumsi kolom 'sma_20' dan 'sma_50' sudah dihitung oleh indicator_calculator
    if 'sma_20' not in result_df.columns or 'sma_50' not in result_df.columns:
        result_df['portfolio_value'] = initial_capital
        return result_df

    # Signal 1 jika SMA 20 > SMA 50 (Uptrend), -1 jika sebaliknya
    result_df['signal'] = np.where(result_df['sma_20'] > result_df['sma_50'], 1, -1)
    
    return _simulate_trades(result_df, initial_capital, fee_rate)

def run_macd_signal(df: pd.DataFrame, initial_capital: float = 100000000.0, fee_rate: float = 0.002) -> pd.DataFrame:
    """Strategi aktif: Beli jika garis MACD di atas garis Sinyal, Jual jika di bawah."""
    result_df = df.copy()
    
    if 'macd' not in result_df.columns or 'macds' not in result_df.columns:
        result_df['portfolio_value'] = initial_capital
        return result_df

    # Signal 1 jika MACD > Signal Line, -1 jika sebaliknya
    result_df['signal'] = np.where(result_df['macd'] > result_df['macds'], 1, -1)
    
    return _simulate_trades(result_df, initial_capital, fee_rate)

def _simulate_trades(df: pd.DataFrame, initial_capital: float, fee_rate: float) -> pd.DataFrame:
    """Fungsi internal untuk mensimulasikan jual/beli berdasarkan kolom 'signal'."""
    cash = initial_capital
    shares = 0
    portfolio_values = []

    # Kita cek pergerakan sinyal hari demi hari
    current_position = 0 # 0 = pegang cash, 1 = pegang saham

    for i in range(len(df)):
        price = df['close'].iloc[i]
        sig = df['signal'].iloc[i]
        
        # Sinyal Buy & Punya Cash
        if sig == 1 and current_position == 0:
            shares_to_buy = (cash * (1 - fee_rate)) // price
            if shares_to_buy > 0:
                cost = shares_to_buy * price
                fee = cost * fee_rate
                cash -= (cost + fee)
                shares = shares_to_buy
                current_position = 1
                
        # Sinyal Sell & Punya Saham
        elif sig == -1 and current_position == 1:
            revenue = shares * price
            fee = revenue * fee_rate
            cash += (revenue - fee)
            shares = 0
            current_position = 0
            
        # Catat total aset harian
        portfolio_values.append(cash + (shares * price))
        
    df['portfolio_value'] = portfolio_values
    return df
