from Bio import SeqIO
import gzip

def retrieve_matching_records(fastq_file, filtered_read_ids):
    matching_records = []

    with gzip.open(fastq_file, 'rt') as file:
        for record in SeqIO.parse(file, 'fastq'):
            for barcode, passed_reads in filtered_read_ids.items():
                if record.id in passed_reads:
                    matching_records.append(record)

    return matching_records