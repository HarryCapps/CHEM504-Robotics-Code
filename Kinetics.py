# Kinetics.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os


def process_and_plot_absorbance(
    csv_path: str,
    reference_time: float = 3.0,
    show_plot: bool = True,
    save_plot_path: str = "kinetics_graph.png",
    save_data_path: str = "Kinetics_data.csv"
) -> pd.DataFrame:
    """
    Processes a CSV containing Time and Blue Pixel Count, normalizes absorbance using the pixel count at a given time,
    fits ln(absorbance) vs. adjusted time to a straight line, and plots it with the slope labeled as -k.
    Saves the plot as 'kinetics_graph.png' and the processed data as 'Kinetics_data.csv' by default unless other paths are specified.

    Parameters:
        csv_path (str): Path to the CSV file.
        reference_time (float): Time (in seconds) to use as reference (default: 3.0).
        show_plot (bool): Whether to display the plot (default: True).
        save_plot_path (str): Path to save the plot (default: 'kinetics_graph.png').
        save_data_path (str): Path to save the processed data (default: 'Kinetics_data.csv').

    Returns:
        pd.DataFrame: DataFrame with added columns for Absorbance, Adjusted Time, and ln(Absorbance).
    """
    csv_path = os.path.expanduser(csv_path)
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    ref_values = df.loc[df['Time (Seconds)'] == reference_time, 'Blue Pixel Count'].values
    if len(ref_values) == 0:
        raise ValueError(f"No data found for Time = {reference_time} Seconds.")
    ref_value = ref_values[0]

    df['Absorbance'] = df['Blue Pixel Count'] / ref_value
    df['Adjusted Time (Seconds)'] = df['Time (Seconds)'] - reference_time
    df['ln(Absorbance)'] = np.log(df['Absorbance'])

    x = df['Adjusted Time (Seconds)']
    y = df['ln(Absorbance)']
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, 'o', label='Data')
    plt.plot(x, slope * x + intercept, 'r-', label=f'Fit: -k = {abs(slope):.4f}')
    plt.title("Determining the Reaction Kinetics of Methylene Blue")
    plt.xlabel("Time (Seconds, adjusted)")
    plt.ylabel("ln(Absorbance)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_plot_path:
        plt.savefig(save_plot_path)
        print(f"Plot saved successfully to: {save_plot_path}")

    if show_plot:
        plt.show()
    else:
        plt.close()

    if save_data_path:
        df.to_csv(save_data_path, index=False)
        print(f"Processed data saved to: {save_data_path}")

    print("Absorbance analysis complete.")
    return df
