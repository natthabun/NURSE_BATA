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
    median_val = statistics.median(lengths)   

    q1 = statistics.quantiles(lengths, n=4)[0]  
    q3 = statistics.quantiles(lengths, n=4)[2]  
    iqr = q3 - q1
    
    return median_val, iqr

def length_n50(lengths):
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
        return None, None  

    lower_value = float(np.percentile(lengths, lower))
    upper_value = float(np.percentile(lengths, upper))

    return lower_value, upper_value