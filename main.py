from G2_PACKAGE.extraction.extracted_data import *
from G2_PACKAGE.calculation.length_calculating import *
from G2_PACKAGE.barcodes_dependent.statistics_by_barcodes import *
from G2_PACKAGE.filtration.filtered_data import * 
from G2_PACKAGE.matching_and_writing.writing_new_file import *
import datetime

# def argparserLocal():
fastq_file= 'data/ont_reads.project.fastq.gz'
#function from extraction
print(data_barcodes_dependent(fastq_file))

#function from calculating saperated by barcode
barcode_statistics = calculate_statistics_by_barcode(fastq_file)
print("Barcode Statistics:" ,barcode_statistics)

#function from filtering
print(filtering_result(fastq_file,55,60,20))

#function from writing new file
output_file = 'new_filtered.fastq.gz'
# print(retrieve_matching_records(fastq_file, filtering_result(fastq_file,55,60,20)))
# write_matching_records_to_fastq(retrieve_matching_records(fastq_file, filtering_result(fastq_file,55,60,30)), output_file)