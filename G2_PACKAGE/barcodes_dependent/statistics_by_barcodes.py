from G2_PACKAGE.extraction.extracted_data import *
from G2_PACKAGE.calculation.length_calculating import *


def list_length(barcodes_dict):
    lengths_per_barcode = {}
    for barcode, records in barcodes_dict.items():
        lengths = [record_data[0] for record_data in records.values()]
        lengths_per_barcode[barcode] = lengths
    return lengths_per_barcode

def calculate_statistics_by_barcode(fastq_file):
    results = {}
    barcodes_dict = data_barcodes_dependent(fastq_file)

    # Get lengths for each barcode
    lengths_per_barcode = list_length(barcodes_dict)

    for barcode, lengths in lengths_per_barcode.items():
        # Calculate statistics for the current barcode
        mean_length, sd_length = mean_sd(lengths)
        max_length, min_length = maxmin_length(lengths)
        median, iqr = median_and_iqr(lengths)
        n50 = length_n50(lengths)

        # Store results in a dictionary for each barcode
        results[barcode] = {
            "mean_length": mean_length,
            "sd_length": sd_length,
            "max_length": max_length,
            "min_length": min_length,
            "median": median,
            "IQR": iqr,
            "N50": n50,
            # "lower_percentile": lower_percentile,
            # "upper_percentile": upper_percentile
        }

    return results