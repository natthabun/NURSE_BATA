from Bio import SeqIO
import gzip
from G2_PACKAGE.matching_and_writing.matching_records import *

def write_matching_records_to_fastq(matching_records, output_file):
    with gzip.open(output_file, 'wt') as file:
        SeqIO.write(matching_records, file, 'fastq')