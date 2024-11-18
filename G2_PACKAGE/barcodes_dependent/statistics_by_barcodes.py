from G2_PACKAGE.extraction.extracted_data import *
from G2_PACKAGE.calculation.length_calculating import *


def list_length(barcodes_dict):
    for barcode, records in barcodes_dict.items():
        lengths = [record_data[0] for record_data in records.values()]
    return lengths

def calculate_statistics_by_barcode(fastq_file):
    results = {}
    barcodes_dict = data_barcodes_dependent(fastq_file)
    for barcode, records in barcodes_dict.items():
        # Extract read lengths from the records
        lengths = list_length(barcodes_dict)  # Assuming `seq_length` is the first element
        # Calculate statistics for the current barcode
        mean_length, sd_length = mean_sd(lengths)
        max_length, min_length = maxmin_length(lengths)
        median, iqr = median_and_iqr(lengths)
        n50 = length_n50(lengths)
        lower_percentile, upper_percentile = length_percentiles(lengths)

        # Store results in a dictionary for each barcode
        results[barcode] = {
            "mean_length": mean_length,
            "sd_length": sd_length,
            "max_length": max_length,
            "min_length": min_length,
            "median": median,
            "IQR": iqr,
            "N50": n50,
        }
    return results