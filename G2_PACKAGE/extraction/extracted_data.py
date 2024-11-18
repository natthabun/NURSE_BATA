import gzip
import numpy as np
from Bio import SeqIO

def data_barcodes_dependent(fastq_file):
    barcodes_dict = {}
    with gzip.open(fastq_file, 'rt') as file:
        for index, record in enumerate(SeqIO.parse(file, 'fastq')):
            Bar_code = record.description.split()[6].split('barcode=')[1].strip()  
            seq_length = len(record.seq)
            avg_score = np.mean(record.letter_annotations['phred_quality'])
            record_data = [seq_length, avg_score]

            if Bar_code not in barcodes_dict:
                barcodes_dict[Bar_code] = {}

            barcodes_dict[Bar_code][record.id] = record_data
            
            # if index == 20000:
                # break
    return barcodes_dict

 

