import statistics
import numpy as np

def maxmin_length(lengths):
    maxval = max(lengths) if lengths else None
    minval = min(lengths) if lengths else None
    return maxval, minval

def mean_sd(lengths):
    mean_length = statistics.mean(lengths)
    sd_length = statistics.stdev(lengths)
    return mean_length, sd_length

def median_and_iqr(lengths):
    #calculating median
    median_val = statistics.median(lengths)   
    #calculating iqr
    q1 = statistics.quantiles(lengths, n=4)[0]  # 25th percentile (Q1)
    q3 = statistics.quantiles(lengths, n=4)[2]  # 75th percentile (Q3)
    iqr = q3 - q1
    
    return median_val, iqr

def calculate_n50(lengths):
    sorted_lengths = sorted(lengths, reverse=True)
    total_length = sum(sorted_lengths)
    cumulative_length = 0
    for length in sorted_lengths:
        cumulative_length += length
        if cumulative_length >= total_length / 2:
            return length
    return None

def length_percentiles(lengths, lower=0, upper=100):
    if not isinstance(lengths, list) or len(lengths) == 0:
        return None, None  # Handle empty or invalid list

    # Calculate lower and upper percentile values using numpy.percentile
    lower_value = float(np.percentile(lengths, lower))
    upper_value = float(np.percentile(lengths, upper))

    return lower_value, upper_value
