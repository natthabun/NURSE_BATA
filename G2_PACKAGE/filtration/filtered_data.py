from G2_PACKAGE.extraction.extracted_data import *
from G2_PACKAGE.calculation.length_calculating import *
from G2_PACKAGE.barcodes_dependent.statistics_by_barcodes import *

def filtering_percentile_result(fastq_file, barcode_percentiles, threshold):
    # Get data for all barcodes
    barcodes_dict = data_barcodes_dependent(fastq_file)
    
    # Prepare the result dictionary
    result = {}
    for barcode, records in barcodes_dict.items():
        passed_read = []  # Reset the passed reads list for each barcode

        if barcode in barcode_percentiles:
            lower_percentile, upper_percentile = barcode_percentiles[barcode]
        else:
            print(f"No percentile range provided for {barcode}. Skipping...")
            continue    # Reset the passed reads list for each barcode
        lengths = [record_data[0] for record_data in records.values()]
        
        # Calculate length percentiles for the current barcode
        lower_length, upper_length = length_percentiles(lengths, lower_percentile, upper_percentile)
        # Filter records based on percentiles and quality score
        for read, data in records.items():
            seq_length, avg_quality = data
            
            # Ensure seq_length and avg_quality are not None
            if seq_length is not None and avg_quality is not None:
                if lower_length <= int(seq_length) <= upper_length and avg_quality >= threshold:
                    passed_read.append(read)
        # Store passed reads for the current barcode
        result[barcode] = passed_read
        
        # Print summary for the current barcode
        print(f"Passed reads from {barcode} - Total: {len(passed_read)}")
        print(passed_read)
    
    return result


def filtering_length_result(fastq_file, barcode_lengths, threshold):
    # Get data for all barcodes
    barcodes_dict = data_barcodes_dependent(fastq_file)
    
    # Prepare the result dictionary
    result = {}
    
    for barcode, records in barcodes_dict.items():
        passed_read = []  # Reset the passed reads list for each barcode

        if barcode in barcode_lengths:
            min_length, max_length = barcode_lengths[barcode]
        else:
            print(f"No length range provided for {barcode}. Skipping...")
            continue  
        
        for read, data in records.items():
            seq_length, avg_quality = data
            if min_length <= int(seq_length) <= max_length and avg_quality >= threshold:
                passed_read.append(read)
        
        # Store passed reads for the barcode
        result[barcode] = passed_read
        
        # Print summary for the barcode
        print(f"Passed reads from {barcode} - Total: {len(passed_read)}")
        print(passed_read)
    return result