from G2_PACKAGE.extraction.extracted_data import *
from G2_PACKAGE.calculation.length_calculating import *
from G2_PACKAGE.barcodes_dependent.statistics_by_barcodes import *

def filtering_percentile_result(fastq_file,lower_percentile, upper_percentile, threshold):
    data_input = data_barcodes_dependent(fastq_file)
    lengths = list_length(data_input)
    lower_length, upper_length = length_percentiles(lengths, lower_percentile, upper_percentile)
    result = {}
    passed_read = []
    for barcode, record in data_input.items():
        for read, data in record.items():
            if lower_length <= int(data[0]) <= upper_length and data[1] >= threshold:   
                passed_read.append(read)
        result[barcode] = passed_read
        print(f"Passed reads from {barcode}", "Total:", len(result[barcode]), result[barcode])
    return result

def filtering_length_result(fastq_file,min_length, max_length, threshold):
    data_input = data_barcodes_dependent(fastq_file)
    lengths = list_length(data_input)
    result = {}
    passed_read = []
    for barcode, record in data_input.items():
        for read, data in record.items():
            if min_length <= int(data[0]) <= max_length and data[1] >= threshold:   
                passed_read.append(read)
        result[barcode] = passed_read
        print(f"Passed reads from {barcode}", "Total:", len(result[barcode]), result[barcode])
    return result

