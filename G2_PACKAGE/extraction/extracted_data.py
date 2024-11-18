import gzip
import numpy as np
from Bio import SeqIO

def data_barcodes_dependent(fastq_file):
    barcodes_dict = {}
    with gzip.open(fastq_file, 'rt') as file:
        for index, record in enumerate(SeqIO.parse(file, 'fastq')):
            # Extract barcode (robust parsing with fallback)
            description_parts = record.description.split()
            barcode_field = next((part for part in description_parts if 'barcode=' in part), None)
            if barcode_field:
                barcode = barcode_field.split('=')[1]
            else:
                barcode = 'unknown'

            # Extract sequence length and average quality score
            seq_length = len(record.seq)
            avg_score = np.mean(record.letter_annotations['phred_quality'])
            record_data = [seq_length, avg_score]

            # Initialize barcode entry if not exists
            if barcode not in barcodes_dict:
                barcodes_dict[barcode] = {}

            # Add record data
            barcodes_dict[barcode][record.id] = record_data
            # if index == 100000:
                # break 
    return barcodes_dict

 

