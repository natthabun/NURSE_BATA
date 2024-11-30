from G2_PACKAGE.extraction.extracted_data import *
from G2_PACKAGE.calculation.length_calculating import *
from G2_PACKAGE.barcodes_dependent.statistics_by_barcodes import *
from G2_PACKAGE.filtration.filtered_data import * 
from G2_PACKAGE.matching_and_writing.writing_new_file import *

def argparserLocal():
    from argparse import ArgumentParser
    parser = ArgumentParser(prog='my_package', description='Work with sequencing data by filtering based on read-quality and sequence-length.')

    subparsers = parser.add_subparsers(
        title='commands', description='Please choose a command below:', dest='command'
    )
    subparsers.required = True

    # Command for showing stats for decision-making
    stats_command = subparsers.add_parser('statAnalysis', help='Perform statistical analysis for decision-making')
    stats_command.add_argument("-f", "--file", type=str, required=True, help="Input FASTQ file")
    stats_command.add_argument("-p", "--percentiles", required=True,type=float, nargs=2,
                                help="Input range of Percentiles for statistical analysis (low, high)")

    # Command for showing filtered data
    filter_command = subparsers.add_parser('filterPreview', help='Preview data filtered based on criteria')
    filter_command.add_argument("-f", "--file", type=str, required=True, help="Input FASTQ file")
    filter_command.add_argument("-t","--filter_type", choices=['percentiles', 'lengths'], required=True, help="Choose filter-type betweem percentiles and lengths")
    filter_command.add_argument("-p", "--percentiles", type=str, nargs='+', metavar='BARCODE:PERCENTILES',
                                help="Percentile thresholds for each barcode, e.g., barcodeID:min-max")
    filter_command.add_argument("-l", "--lengths", type=str, nargs='+', metavar='BARCODE:LENGTHS',
                                help="Length thresholds for each barcode, e.g., barcodeID:min-max")
    filter_command.add_argument("-q", "--qscore", type=int, required=True, help="Input Phred quality scores (Q) threshold")

    # Command for writing new filtered file
    write_command = subparsers.add_parser('exportData', help='Export filtered data to a new file')
    write_command.add_argument("-f", "--file", type=str, required=True, help="Input FASTQ file")
    write_command.add_argument("-n", "--new_file", type=str, required=True, help="Provide a name for the new file to save the filtered data")
    write_command.add_argument("-t","--filter_type", choices=['percentiles', 'lengths'], required=True, help="Choose filter-type betweem percentiles and lengths")
    write_command.add_argument("-p", "--percentiles", type=str, nargs='+', metavar='BARCODE:PERCENTILES',
                                help="Percentile thresholds for each barcode, e.g., barcodeID:min-max")
    write_command.add_argument("-l", "--lengths", type=str, nargs='+', metavar='BARCODE:LENGTHS',
                                help="Length thresholds for each barcode, e.g., barcodeID:min-max")
    write_command.add_argument("-q", "--qscore", type=int, required=True, help="Input Phred quality scores (Q) threshold")

    return parser

def show_stats(file, percentiles):
    print(f"Showing statistical data from {file} with percentiles {percentiles}...")
    stats_result = calculate_statistics_by_barcode(file, percentiles[0], percentiles[1])
    print(stats_result)

    return stats_result

def parse_barcode_input(barcode_input):
    separated_barcode = {}
    for each_input in barcode_input:
        if ':' not in each_input or '-' not in each_input:
            raise ValueError(f"Invalid format for barcode: {each_input}. Expected 'barcodeID:min-max'")
        barcode, values = each_input.split(':')
        lower_value, upper_value = map(int, values.split('-'))
        
        if lower_value > upper_value:
            raise ValueError(f"Min value cannot be greater than max value for barcode {barcode}: {each_input}")
        separated_barcode[barcode] = (lower_value, upper_value)
    
    return separated_barcode

def show_filtered_percentile_data(file, percentiles_input, qscore_threshold):
    barcode_percentiles = parse_barcode_input(percentiles_input)
    print(f"Showing filtered data from {file} with the following percentiles thresholds: {barcode_percentiles} and quality score threshold {qscore_threshold}...")
    filtered_result = filtering_percentile_result(file, barcode_percentiles, qscore_threshold)
    return filtered_result


def show_filtered_length_data(file, lengths_input, qscore_threshold):
    barcode_lengths = parse_barcode_input(lengths_input)
    print(f"Showing filtered data from {file} with the following length thresholds: {barcode_lengths} and quality score threshold {qscore_threshold}...")
    filtered_result = filtering_length_result(file, barcode_lengths, qscore_threshold)
    return filtered_result

def write_filtered_percentile_file(file, new_file_name, percentiles_input, qscore_threshold):
    barcode_percentiles = parse_barcode_input(percentiles_input)
    print(f"Writing filtered data from {file} to {new_file_name} with percentiles {barcode_percentiles} and quality score threshold = {qscore_threshold}...")
    new_file = write_matching_records_to_fastq(retrieve_matching_records(file, filtering_percentile_result(file,barcode_percentiles, qscore_threshold)), new_file_name)
    return new_file

def write_filtered_length_file(file, new_file_name, lengths_input, qscore_threshold):
    barcode_lengths = parse_barcode_input(lengths_input)
    print(f"Writing filtered data from {file} to {new_file_name} between length {barcode_lengths} and quality score threshold {qscore_threshold}...")
    new_file = write_matching_records_to_fastq(retrieve_matching_records(file, filtering_length_result(file,barcode_lengths, qscore_threshold)), new_file_name)
    return new_file

def main():
    parser = argparserLocal()
    args = parser.parse_args()

    print("Process is proceeding")

    if args.command == 'statAnalysis':
        show_stats(args.file, args.percentiles)

    elif args.command == 'filterPreview':
        if args.filter_type == 'percentiles':
            show_filtered_percentile_data(args.file, args.percentiles, args.qscore)
        else:
            show_filtered_length_data(args.file, args.lengths, args.qscore)
    elif args.command == 'exportData':
        if args.filter_type == 'percentiles':
            write_filtered_percentile_file(args.file, args.new_file, args.percentiles, args.qscore)
        else:
            write_filtered_length_file(args.file, args.new_file, args.lengths, args.qscore)

    print("Process is completed")


if __name__ == "__main__":
    main()
