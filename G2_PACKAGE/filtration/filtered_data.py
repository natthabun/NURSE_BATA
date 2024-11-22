from G2_PACKAGE.extraction.extracted_data import *
from G2_PACKAGE.calculation.length_calculating import *
from G2_PACKAGE.barcodes_dependent.statistics_by_barcodes import *
from tabulate import tabulate
import pandas as pd

def filtering_percentile_result(fastq_file, barcode_percentiles, threshold):
    barcodes_dict = data_barcodes_dependent(fastq_file)

    result = {}
    
    for barcode, records in barcodes_dict.items():
        passed_read = []  
        if barcode in barcode_percentiles:
            lower_percentile, upper_percentile = barcode_percentiles[barcode]
        else:
            print(f"No percentile range provided for {barcode}. Skipping...")
            continue    
        lengths = [record_data[0] for record_data in records.values()]
        lower_length, upper_length = length_percentiles(lengths, lower_percentile, upper_percentile)
        for read, data in records.items():
            seq_length, avg_quality = data
            if seq_length is not None and avg_quality is not None:
                if lower_length <= int(seq_length) <= upper_length and avg_quality >= threshold:
                    passed_read.append(read)

        result[barcode] = passed_read
 
        print(f"Passed reads from {barcode} - Total: {len(passed_read)}")
  
    df = pd.DataFrame.from_dict(result, orient="index").transpose()
    df.columns = result.keys()
    df.index = range(1, len(df) + 1)

    table = tabulate(df, headers="keys", tablefmt="pretty")
    print(table)

    return result
    


def filtering_length_result(fastq_file, barcode_lengths, threshold):
    barcodes_dict = data_barcodes_dependent(fastq_file)

    result = {}
    
    for barcode, records in barcodes_dict.items():
        passed_read = []  

        if barcode in barcode_lengths:
            min_length, max_length = barcode_lengths[barcode]
        else:
            print(f"No length range provided for {barcode}. Skipping...")
            continue  
        
        for read, data in records.items():
            seq_length, avg_quality = data
            if min_length <= int(seq_length) <= max_length and avg_quality >= threshold:
                passed_read.append(read)
       
        result[barcode] = passed_read
     
        print(f"Passed reads from {barcode} - Total: {len(passed_read)}")

    df = pd.DataFrame.from_dict(result, orient="index").transpose()
    df.columns = result.keys()
    df.index = range(1, len(df) + 1)

    table = tabulate(df, headers="keys", tablefmt="pretty")
    print(table)
    
    return result