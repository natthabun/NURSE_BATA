from G2_PACKAGE.extraction.extracted_data import *
from G2_PACKAGE.calculation.length_calculating import *
from G2_PACKAGE.barcodes_dependent.statistics_by_barcodes import *
from G2_PACKAGE.filtration.filtered_data import * 
from G2_PACKAGE.matching_and_writing.writing_new_file import *

def argparserLocal():
    from argparse import ArgumentParser
    parser = ArgumentParser(prog='my_package', description='Work with sequence filtering')

    subparsers = parser.add_subparsers(
        title='commands', description='Please choose a command below:', dest='command'
    )
    subparsers.required = True

    # Command for showing stats for decision-making
    stats_command = subparsers.add_parser('showStats', help='Show statistics for decision-making')
    stats_command.add_argument("-f", "--file", type=str, required=True, help="Input FASTQ file")
    stats_command.add_argument("-p", "--percentiles", required=True,type=float, nargs=2,
                                help="Percentiles for statistics (low, high)")

    # Command for showing filtered data
    filter_command = subparsers.add_parser('showFiltered', help='Show filtered data based on criteria')
    filter_command.add_argument("-f", "--file", type=str, required=True, help="Input FASTQ file")
    filter_command.add_argument("-t","--filter_type", choices=['percentiles', 'length'], required=True, help="Filter type to apply")
    filter_command.add_argument("-p", "--percentiles", type=float, nargs=2,
                                help="Percentiles for filtering (low, high)")
    filter_command.add_argument("-l", "--lengths", type=str, nargs='+', metavar='BARCODE:LENGTHS',
                                help="Length thresholds for each barcode, e.g., barcodeID:min-max")
    filter_command.add_argument("-q", "--qscore", type=int, required=True, help="Quality score threshold")

    # Command for writing new filtered file
    write_command = subparsers.add_parser('writeFiltered', help='Write filtered data to a new file')
    write_command.add_argument("-f", "--file", type=str, required=True, help="Input FASTQ file")
    write_command.add_argument("-n", "--new_file", type=str, required=True, help="New file name for filtered data")
    write_command.add_argument("-t","--filter_type", choices=['percentiles', 'length'], required=True, help="Filter type to apply")
    write_command.add_argument("-p", "--percentiles", type=float, nargs=2,
                               help="Percentiles for filtering (low, high)")
    write_command.add_argument("-l", "--lengths", type=str, nargs='+', metavar='BARCODE:LENGTHS',
                                help="Length thresholds for each barcode, e.g., barcodeID:min-max")
    write_command.add_argument("-q", "--qscore", type=int, required=True, help="Quality score threshold")

    return parser

def show_stats(file, percentiles):
    print(f"Showing statistics for {file} with percentiles {percentiles}...")
    stats_result = calculate_statistics_by_barcode(file, percentiles[0], percentiles[1])
    print("Barcode Statistics:" , stats_result)

    return stats_result

def show_filtered_percentile_data(file, percentiles, qscore_threshold):
    print(f"Showing filtered data from {file} with percentiles {percentiles} and quality score threshold {qscore_threshold}...")
    filtered_result = filtering_percentile_result(file, percentiles[0], percentiles[1], qscore_threshold)
    return filtered_result

def parse_barcode_lengths(lengths_input):
    barcode_lengths = {}
    for each_input in lengths_input:
        if ':' not in each_input or '-' not in each_input:
            raise ValueError(f"Invalid format for barcode length: {each_input}. Expected 'barcodeID:min-max'")
        barcode, lengths = each_input.split(':')
        min_length, max_length = map(int, lengths.split('-'))
        
        if min_length > max_length:
            raise ValueError(f"Min length cannot be greater than max length for barcode {barcode}: {each_input}")
        barcode_lengths[barcode] = (min_length, max_length)
    
    return barcode_lengths

def show_filtered_length_data(file, lengths_input, qscore_threshold):
    barcode_lengths = parse_barcode_lengths(lengths_input)
    print(f"Showing filtered data from {file} with the following length thresholds: {barcode_lengths} and quality score threshold {qscore_threshold}...")
    # Get the filtered result based on the barcode-specific length thresholds and quality score
    filtered_result = filtering_length_result(file, barcode_lengths, qscore_threshold)
    return filtered_result

def write_filtered_percentile_file(file, new_file_name, percentiles, qscore_threshold):
    print(f"Writing filtered data from {file} to {new_file_name} with percentiles {percentiles} and quality score threshold {qscore_threshold}...")
    new_file = write_matching_records_to_fastq(retrieve_matching_records(file, filtering_percentile_result(file,percentiles[0], percentiles[1], qscore_threshold)), new_file_name)
    return new_file

def write_filtered_length_file(file, new_file_name, lengths_input, qscore_threshold):
    barcode_lengths = parse_barcode_lengths(lengths_input)
    print(f"Writing filtered data from {file} to {new_file_name} between length {barcode_lengths} and quality score threshold {qscore_threshold}...")
    new_file = write_matching_records_to_fastq(retrieve_matching_records(file, filtering_length_result(file,barcode_lengths, qscore_threshold)), new_file_name)
    return new_file

def main():
    parser = argparserLocal()
    args = parser.parse_args()
    print("Process is proceeding")
    if args.command == 'showStats':
        show_stats(args.file, args.percentiles)

    elif args.command == 'showFiltered':
        if args.filter_type == 'percentiles':
            show_filtered_percentile_data(args.file, args.percentiles, args.qscore)
        else:
            show_filtered_length_data(args.file, args.lengths, args.qscore)
    elif args.command == 'writeFiltered':
        if args.filter_type == 'percentiles':
            write_filtered_percentile_file(args.file, args.new_file, args.percentiles, args.qscore)
        else:
            write_filtered_length_file(args.file, args.new_file, args.lengths, args.qscore)
    print("Process is completed")


if __name__ == "__main__":
    main()
