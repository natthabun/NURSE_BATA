# Project Overview
This project allows users to filter sequencing reads from FASTQ files based on customizable criteria. The script provides flexible filtering options, enabling users to specify either exact length ranges or percentiles for filtering, along with a global quality score threshold.

# Features
Length-Based Filtering: Users can specify an exact length range (minimum and maximum) for reads in each barcode.

Percentile-Based Filtering: Users can define percentile thresholds (e.g., 30th to 80th percentile) to filter read lengths for each barcode.

Quality Score Threshold: Users can apply a global quality score threshold that applies to all barcodes.

Barcode-Specific Filtering: The tool allows users to define different length ranges or percentiles for each barcode individually.

Detailed Output:

Filtered reads are written to a new FASTQ file for downstream analysis.
Results are summarized in a table format for easy interpretation.

# How to Set Up the Environment
Use the provided G2_environment.yml file to set up the required environment
## Dependencies
name: g2project_env
channels:
  - conda-forge
  - bioconda
  - defaults
dependencies:
  - python=3.9
  - pandas
  - numpy
  - biopython
  - tabulate
  - pip
  - pip:
      - statistics
## Commands to set up the environment
conda env create -f G2_environment.yml

conda activate g2project_env

# How to Use
1. Input
FASTQ File: A gzipped FASTQ file containing sequence reads.
Filtering Options:
Length-based: Specify exact ranges using the format barcodeID:min-max (e.g., barcode01:100-200).
Percentile-based: Specify percentile ranges using the same format, e.g., barcode01:30-80.
Quality Score: Set a global quality score threshold for all reads, e.g., 20.
2. Output
A new FASTQ file containing only the filtered reads.
A summary table showing the number of passed reads along with their read id for each barcode.

# Command-Line Example
## Show the overall

To using ‘./my_package -h’ you have to change permission first using ‘chmod +x my_package’ or you can run using python main.py -h as well

Showing help message for each one

./my_package statAnalysis -h

./my_package filterPreview -h

./my_package exportData -h

## Showing the statistics for each barcode for decision-making

./my_package statAnalysis -f original_file.fastq.gz -p 10 90

### arguments:

-f , --file : Input FASTQ file

-p , --percentiles : Input range of Percentiles for statistical analysis (low, high)
                        
## Filtering Reads by Percentiles for Barcode 01 and Barcode 02

./my_package filterPreview -f original_file.fastq.gz -t percentiles -p barcode01:20-80 barcode02:10-90 -q 30

## Filtering Reads by Lengths for Barcode 01 and Barcode 02

./my_package filterPreview -f original_file.fastq.gz -t lengths -l barcode01:2000-8000 barcode02:1000-9000 -q 30

### arguments:

-f, --file : Input FASTQ file

-t {percentiles,lengths}, --filter_type {percentiles,lengths} : Choose filter-type between percentiles and lengths

-p BARCODE:PERCENTILES, --percentiles BARCODE:PERCENTILES
                    :   Percentile thresholds for each barcode, e.g., barcodeID:min-max

-l BARCODE:LENGTHS, --lengths BARCODE:LENGTHS 
                     :   Length thresholds for each barcode, e.g., barcodeID:min-max

-q , --qscore 
                     :   Input Phred quality scores (Q) threshold

## Retrieve Filtered Reads and Save to a FASTQ File
### Writng new Reads file by Percentiles for Barcode 01 and Barcode 02  
./my_package exportData -f original_file.fastq.gz -n new_file.fastq -t percentiles -p barcode01:20-80 barcode02:10-90 -q 30

## Writing new Reads file by Lengths for Barcode 01 and Barcode 02  
  
./my_package exportData -f original_file.fastq.gz -n new_file.fastq -t lengths -l barcode01:2000-8000 barcode02:1000-9000 -q 30

### Arguments:

-f, --file : Input FASTQ file
  
-n, --new_file
            :            Provide a name for the new file to save the filtered data
  
-t {percentiles,lengths}, --filter_type {percentiles,lengths}
             :           Choose filter-type between percentiles and lengths

-p BARCODE:PERCENTILES, --percentiles BARCODE:PERCENTILES 
            :            Percentile thresholds for each barcode, e.g., barcodeID:min-max

-l BARCODE:LENGTHS, --lengths BARCODE:LENGTHS
           :             Length thresholds for each barcode, e.g., barcodeID:min-max
  
-q, --qscore 
           :             Input Phred quality scores (Q) threshold




