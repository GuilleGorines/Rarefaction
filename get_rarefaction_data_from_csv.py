# /usr/bin/env python
'''
=============================================================
HEADER
=============================================================
INSTITUTION: BU-ISCIII

AUTHOR: Guillermo J. Gorines Cordero
MAIL: guillermo.gorines@urjc.es
VERSION: 1 
CREATED: 17-01-2023
REVISED: 17-01-2023
REVISED BY: Guillermo J. Gorines Cordero

DESCRIPTION: 
    *insert description, third person*
INPUT (by order):
    1. CSV file
    2. prefix for the outfiles to have
OUTPUT:

USAGE:
    python get_rarefaction_data.py 
                            --csv CSV_FILE
                            --out-prefix OUT_PREFIX

REQUIREMENTS:
    -Python >= 3.6

DISCLAIMER:

TO DO: 

================================================================
END_OF_HEADER
================================================================
'''
import sys
import argparse
import json
from statistics import quantiles, mean

def parse_args(args=None):
    """
    Parse the args
    """
    Description = "Simple script to obtain the rarefaction curve data for individual samples"
    Epilog = "Example usage: python get_rarefaction_data.py --csv JSONP_FILE --out-prefix OUT_PREFIX --iterations ITERATION_NUMBER"

    parser = argparse.ArgumentParser(description=Description, epilog=Epilog)

    parser.add_argument(
                        "--csv",
                        help="CSV file obtained from the rarefaction curve data",
                        required=True,
                        dest="csv"
                        )

    parser.add_argument(
                        "--out-prefix",
                        help="Name of the outfile where the data will be placed",
                        required=True,
                        dest="out_prefix"
                        )

    parser.add_argument(
                        "--iterations",
                        help="Number of iterations of rarefaction for each depth",
                        default=10,
                        dest="iterations"
                        )
    
    parser.add_argument(
                        "--method",
                        help="Method to choose the calculation: median or mean.",
                        required=True,
                        choices=["median", "mean"],
                        dest="method"
                        )

    return parser.parse_args(args)


def load_csv(file):
    """
    Open the CSV file
    Split it using "," as the separator
    """
    with open(file, "r") as infile:
        infile = infile.readlines()

    infile = [item.split(",") for item in infile] 
    
    return infile


def extract_headers(steps_list):
    """
    Get the headers
    schema of the headers is: "depth-1_iter-1", so to get only the depth we:
        Remove the "depth-1"
        Split by "_" so we get [1,_iter-1]
        Capture the first element, 1.
        We use a set comprehension so repeated items will be removed
        Lastly, we add a "samples\depth" in the first element
    """

    headers_list = list({int(item.replace("depth-","").split("_")[0]) for item in steps_list[0][1:] if "iter" in item})
    headers_list.insert(0,"samples\depth")

    return headers_list


def get_stats_data(steps_list, method, iter_number=10):
    """
    Note on functioning:
        lower_limit starts in 1 because 0 is the samplename
        upper_limit starts in 1 + iter_number so its always {iter_number} superior to the lower limit
        The idea is moving in a window with size {iter_number} for each of the rows
        Probably not the most elegant or effective approach, but thats what I have come up with
        NOTE: stat_data corresponds to the median or the mean
    """
    all_median_list = []

    for row in steps_list[1:]:
        
        # First item: samplename
        section_median_list = [row[0]]
        lower_section_limit = 1
        
        for upper_section_limit in range(1+iter_number, len(row)+1, iter_number):
            
            section = row[lower_section_limit:upper_section_limit]

            # if its not divisible by {iter_number}, 
            # its the metadata at the end
            # so we just ignore it
            # Im not really sure thats necessary, it just wont print but anyway
            if len(section) == iter_number:
                if method == "median":
                    first_quartile, stat_data, third_quartile = quantiles([int(x) for x in section], n=4, method="exclusive")
                elif method == "mean":
                    stat_data = mean([int(x) for x in section])

                section_median_list.append(stat_data)
                lower_section_limit += iter_number

        all_median_list.append(section_median_list)

    return all_median_list


def create_tsv(headers, median_list, out_prefix):
    """
    Write nested list to CSV
    Change . with , for decimals
    """
    with open(f"{out_prefix}.tsv", "w") as outfile:

        outfile.write("\t".join([str(item) for item in headers]))
        outfile.write("\n")

        for row in median_list:
            outfile.write("\t".join([str(item).replace(".",",") for item in row]))
            outfile.write("\n")
    return


def main(args=None):
    """
    Full process:
        -Load CSV
        -Get the median for each iteration on each category
        -Generate the tsv file as output
    """
    args = parse_args(args)
    data_list = load_csv(args.csv)

    headers = extract_headers(data_list)

    median_list = get_stats_data(data_list, method=args.method ,iter_number=args.iterations)
    create_tsv(headers, median_list, args.out_prefix)

if __name__ == "__main__":
    sys.exit(main())
