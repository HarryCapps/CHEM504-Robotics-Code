import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

def process_and_plot_absorbance(csv_path: str, reference_time: float = 3.0, show_plot: bool = True) -> pd.DataFrame:
    """
    Processes a CSV containing Time and Blue Pixel Count, normalizes absorbance using the pixel count at a given time,
    fits ln(absorbance) vs. adjusted time to a straight line, and plots it with the slope labeled as -k.

    Parameters:
        csv_path (str): Path to the CSV file.
        reference_time (float): Time (in seconds) to use as reference (default: 3.0).
        show_plot (bool): Whether to display the plot (default: True).

    Returns:
        pd.DataFrame: DataFrame with added columns for Absorbance, Adjusted Time, and ln(Absorbance).
    """
    csv_path = os.path.expanduser(csv_path)
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    ref_values = df.loc[df['Time (seconds)'] == reference_time, 'Blue Pixel Count'].values
    if len(ref_values) == 0:
        raise ValueError(f"No data found for Time = {reference_time} seconds.")
    ref_value = ref_values[0]

    df['Absorbance'] = df['Blue Pixel Count'] / ref_value
    df['Adjusted Time (seconds)'] = df['Time (seconds)'] - reference_time
    df['ln(Absorbance)'] = np.log(df['Absorbance'])

    # Linear regression on ln(absorbance) vs adjusted time
    x = df['Adjusted Time (seconds)']
    y = df['ln(Absorbance)']
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    # Plot
    if show_plot:
        plt.figure(figsize=(8, 5))
        plt.plot(x, y, 'o', label='Data')
        plt.plot(x, slope * x + intercept, 'r-', label=f'Fit: -k = {abs(slope):.4f}')
        plt.title("ln(Absorbance) vs Time")
        plt.xlabel("Time (seconds, adjusted)")
        plt.ylabel("ln(Absorbance)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return df
