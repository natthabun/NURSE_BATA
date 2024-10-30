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

    # Command for showing filtered data
    filter_command = subparsers.add_parser('showFiltered', help='Show filtered data based on criteria')
    filter_command.add_argument("-f", "--file", type=str, required=True, help="Input FASTQ file")
    filter_command.add_argument("-p", "--percentiles", type=float, nargs=2, required=True,
                                help="Percentiles for filtering (low, high)")
    filter_command.add_argument("-q", "--qscore", type=int, required=True, help="Quality score threshold")

    # Command for writing new filtered file
    write_command = subparsers.add_parser('writeFiltered', help='Write filtered data to a new file')
    write_command.add_argument("-f", "--file", type=str, required=True, help="Input FASTQ file")
    write_command.add_argument("-n", "--new_file", type=str, required=True, help="New file name for filtered data")
    write_command.add_argument("-p", "--percentiles", type=float, nargs=2, required=True,
                               help="Percentiles for filtering (low, high)")
    write_command.add_argument("-q", "--qscore", type=int, required=True, help="Quality score threshold")

    return parser

def show_stats(file):
    print(f"Showing statistics for {file}...")
    stats_result = calculate_statistics_by_barcode(file)
    print("Barcode Statistics:" , stats_result)

    return stats_result

def show_filtered_data(file, percentiles, qscore_threshold):
    print(f"Showing filtered data from {file} with percentiles {percentiles} and quality score threshold {qscore_threshold}...")
    filtered_result = filtering_result(file, percentiles[0], percentiles[1], qscore_threshold)
    return filtered_result

def write_filtered_file(file, new_file_name, percentiles, qscore_threshold):
    print(f"Writing filtered data from {file} to {new_file_name} with percentiles {percentiles} and quality score threshold {qscore_threshold}...")
    new_file = write_matching_records_to_fastq(retrieve_matching_records(file, filtering_result(file,percentiles[0], percentiles[1], qscore_threshold)), new_file_name)
    return new_file

def main():
    parser = argparserLocal()
    args = parser.parse_args()
    
    if args.command == 'showStats':
        show_stats(args.file)

    elif args.command == 'showFiltered':
        show_filtered_data(args.file, args.percentiles, args.qscore)

    elif args.command == 'writeFiltered':
        write_filtered_file(args.file, args.new_file, args.percentiles, args.qscore)

if __name__ == "__main__":
    print("Process is proceeding")
    main()
    print("Process is completed")
