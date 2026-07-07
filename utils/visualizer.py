import matplotlib.pyplot as plt
import os

def plot_performance(dates: list, mas_nav: list, bh_nav: list, ticker: str, output_path: str = "results/backtest_plot.png"):
    """
    Plot the performance of MAS vs Buy-and-Hold and save to a PNG file.
    
    Args:
        dates: list of str, date strings
        mas_nav: list of float, Net Asset Value of MAS portfolio
        bh_nav: list of float, Net Asset Value of Buy and Hold portfolio
        ticker: str, the stock ticker
        output_path: str, path to save the plot
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    
    # Plot MAS NAV
    plt.plot(dates, mas_nav, label=f"MAS Agent (NAV)", color="blue", linewidth=2)
    
    # Plot Buy and Hold NAV
    plt.plot(dates, bh_nav, label=f"Buy and Hold (NAV)", color="gray", linestyle="--", linewidth=2)
    
    plt.title(f"Performance Comparison: Multi-Agent System vs Buy-and-Hold ({ticker})")
    plt.xlabel("Date")
    plt.ylabel("Net Asset Value (IDR)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Rotate x-axis labels if there are many dates
    if len(dates) > 10:
        plt.xticks(range(0, len(dates), len(dates)//10), rotation=45)
    else:
        plt.xticks(rotation=45)
        
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved successfully to {output_path}")
    
    plt.close()
