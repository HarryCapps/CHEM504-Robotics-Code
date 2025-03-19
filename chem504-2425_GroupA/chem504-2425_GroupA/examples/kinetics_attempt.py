import time
import math
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper

# Define file paths
csv_file_path = os.path.expanduser("~/Code/chem504-2425_GroupA/examples/blue_pixel_data.csv")
rate_constant_file = os.path.expanduser("~/Code/chem504-2425_GroupA/examples/rate_constant.txt")
graph_file = os.path.expanduser("~/Code/chem504-2425_GroupA/examples/kinetic_analysis_plot.png")

def read_and_process_csv(file_path):
    """Reads CSV file containing time and blue pixel count data."""
    try:
        # Load CSV file
        data = pd.read_csv(file_path)

        # Extract time and intensity (blue pixel count)
        time_values = data.iloc[:, 0].values  # First column = Time (seconds)
        intensity_values = data.iloc[:, 1].values  # Second column = Blue Pixel Count

        # Ensure valid values exist
        if len(time_values) < 2 or len(intensity_values) < 2:
            print("Error: Not enough data points in the CSV file.")
            return None, None

        # Remove NaN, Inf, or negative values
        valid_indices = ~np.isnan(intensity_values) & ~np.isinf(intensity_values) & (intensity_values >= 0)
        time_values = time_values[valid_indices]
        intensity_values = intensity_values[valid_indices]

        if len(time_values) < 2:
            print("Error: Insufficient valid data points after filtering.")
            return None, None

        # ✅ Stop analysis if all intensity values are zero
        if np.all(intensity_values == 0):
            print("No blue pixels detected. No reaction occurred. Skipping analysis.")
            return None, None

        # Normalize intensity values
        max_intensity = max(intensity_values)
        concentration_values = intensity_values / max_intensity if max_intensity > 0 else intensity_values

        return time_values, concentration_values

    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None, None

def zero_order_model(t, k, C0):
    """Zero-order reaction model: C = C0 - k*t"""
    return C0 - k * t

def first_order_model(t, k, C0):
    """First-order reaction model: ln(C) = ln(C0) - k*t"""
    return C0 * np.exp(-k * t)

def second_order_model(t, k, C0):
    """Second-order reaction model: 1/C = 1/C0 + k*t"""
    return 1 / (1/C0 + k * t)

def fit_kinetics(time_values, concentration_values):
    """Fits experimental data to zero-order, first-order, and second-order models and determines the best fit."""

    if len(time_values) < 2 or len(concentration_values) < 2:
        print("Error: Not enough data points for curve fitting.")
        return None, None

    # Remove NaN, Inf, and Zero values
    valid_indices = ~np.isnan(concentration_values) & ~np.isinf(concentration_values) & (concentration_values > 0)
    time_values = time_values[valid_indices]
    concentration_values = concentration_values[valid_indices]

    if len(time_values) < 2:
        print("Error: Insufficient valid data points after filtering.")
        return None, None

    C0 = concentration_values[0]

    try:
        # Fit Zero-Order Model
        popt_zero, _ = curve_fit(zero_order_model, time_values, concentration_values, p0=[0.01, C0])

        # Fit First-Order Model
        popt_first, _ = curve_fit(first_order_model, time_values, concentration_values, p0=[0.01, C0])

        # Fit Second-Order Model (Check for Zero Concentrations Before Taking Reciprocal)
        if np.all(concentration_values > 0):
            popt_second, _ = curve_fit(second_order_model, time_values, 1/concentration_values, p0=[0.01, C0])
            k_second, _ = popt_second
        else:
            print("Skipping Second-Order Fit: Concentration contains zero values.")
            k_second = None

        # Extract rate constants
        k_zero, _ = popt_zero
        k_first, _ = popt_first

        # Determine best-fit model
        best_model, best_k, best_fit_func = None, None, None
        best_r_squared = -np.inf  # To track best fit

        models = [
            ("Zero-Order", k_zero, zero_order_model),
            ("First-Order", k_first, first_order_model),
            ("Second-Order", k_second, second_order_model) if k_second is not None else None
        ]

        for model in models:
            if model:
                model_name, k_value, fit_func = model
                residuals = concentration_values - fit_func(time_values, k_value, C0)
                ss_tot = np.sum((concentration_values - np.mean(concentration_values)) ** 2)
                r_squared = 1 - (np.sum(residuals ** 2) / ss_tot)

                if r_squared > best_r_squared:
                    best_r_squared = r_squared
                    best_model = model_name
                    best_k = k_value
                    best_fit_func = fit_func

        # Print results
        print(f"Best Fit Model: {best_model}")
        print(f"Rate Constant (k): {best_k:.5f}")

        # Save rate constant to a text file
        with open(rate_constant_file, "w") as file:
            file.write(f"Best Fit Model: {best_model}\n")
            file.write(f"Rate Constant (k): {best_k:.5f}\n")

        print(f"Rate constant saved to: {rate_constant_file}")

        # Plot and save graph
        plt.figure(figsize=(8,6))
        plt.scatter(time_values, concentration_values, label="Experimental Data", color="blue")
        plt.plot(time_values, best_fit_func(time_values, best_k, C0), 'r-', label=f"Best Fit ({best_model})")

        plt.xlabel("Time (s)")
        plt.ylabel("Normalized Concentration")
        plt.title(f"Kinetic Analysis - {best_model} Model")
        plt.legend()
        plt.grid()

        plt.savefig(graph_file)
        print(f"Graph saved to: {graph_file}")

        plt.show()

        return best_k, best_model

    except Exception as e:
        print(f"Error in curve fitting: {e}")
        return None, None

def analyze_kinetics(file_path):
    """Reads data from CSV and determines reaction rate constant."""
    time_values, concentration_values = read_and_process_csv(file_path)
    
    # ✅ Stop if no valid data is found
    if time_values is None or concentration_values is None:
        print("Skipping kinetic analysis due to insufficient data.")
        return
    
    return fit_kinetics(time_values, concentration_values)

# Run analysis after reaction data is saved
analyze_kinetics(csv_file_path)
