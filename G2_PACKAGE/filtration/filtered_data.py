from G2_PACKAGE.extraction.extracted_data import *
from G2_PACKAGE.calculation.length_calculating import *
from G2_PACKAGE.barcodes_dependent.statistics_by_barcodes import *

# def filtering_percentile_result(fastq_file,lower_percentile, upper_percentile, threshold):
#     data_input = data_barcodes_dependent(fastq_file)
#     lengths = list_length(data_input)
#     lower_length, upper_length = length_percentiles(lengths, lower_percentile, upper_percentile)
#     result = {}
#     passed_read = []
#     for barcode, record in data_input.items():
#         for read, data in record.items():
#             if lower_length <= int(data[0]) <= upper_length and data[1] >= threshold:   
#                 passed_read.append(read)
#         result[barcode] = passed_read
#         print(f"Passed reads from {barcode}", "Total:", len(result[barcode]), result[barcode])
#     return result

# def filtering_length_result(fastq_file,min_length, max_length, threshold):
#     data_input = data_barcodes_dependent(fastq_file)
#     lengths = list_length(data_input)
#     result = {}
#     passed_read = []
#     for barcode, record in data_input.items():
#         for read, data in record.items():
#             if min_length <= int(data[0]) <= max_length and data[1] >= threshold:   
#                 passed_read.append(read)
#         result[barcode] = passed_read
#         print(f"Passed reads from {barcode}", "Total:", len(result[barcode]), result[barcode])
#     return result

def filtering_percentile_result(fastq_file, lower_percentile, upper_percentile, threshold):
    # Get data for all barcodes
    data_input = data_barcodes_dependent(fastq_file)
    
    # Prepare the result dictionary
    result = {}
    for barcode, records in data_input.items():
        # Extract sequence lengths for the current barcode
        lengths = [data[0] for data in records.values()]  # Extract lengths
        
        # Calculate percentiles for the current barcode
        lower_length, upper_length = length_percentiles(lengths, lower_percentile, upper_percentile)
        
        passed_read = []  # Reset the passed reads list for each barcode
        
        # Filter records based on percentiles and quality score
        for read, data in records.items():
            seq_length, avg_quality = data
            if lower_length <= int(seq_length) <= upper_length and avg_quality >= threshold:
                passed_read.append(read)
        
        # Store passed reads for the current barcode
        result[barcode] = passed_read
        
        # Print summary for the current barcode
        print(f"Passed reads from {barcode} - Total: {len(passed_read)}")
        print(passed_read)
    
    return result


# def filtering_length_result(fastq_file, min_length, max_length, threshold):
#     # Get data for all barcodes
#     data_input = data_barcodes_dependent(fastq_file)
    
#     # Prepare the result dictionary
#     result = {}
    
#     for barcode, records in data_input.items():
#         passed_read = []  # Reset the passed reads list for each barcode
        
#         for read, data in records.items():
#             seq_length, avg_quality = data
#             if min_length <= int(seq_length) <= max_length and avg_quality >= threshold:
#                 passed_read.append(read)
        
#         # Store passed reads for the barcode
#         result[barcode] = passed_read
        
#         # Print summary for the barcode
#         print(f"Passed reads from {barcode} - Total: {len(passed_read)}")
#         print(passed_read)
#     return result
