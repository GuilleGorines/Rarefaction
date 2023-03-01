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
    1. JSONP file
    2. prefix for the outfiles to have
OUTPUT:

USAGE:
    python get_rarefaction_data.py 
                            --jsonp JSONP_FILE 
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
from statistics import mean

def parse_args(args=None):
    """
    Parse the args
    """
    Description = "Simple script to obtain the rarefaction curve data"
    Epilog = "Example usage: python get_rarefaction_data.py --jsonp JSONP_FILE --out-prefix OUT_PREFIX"

    parser = argparse.ArgumentParser(description=Description, epilog=Epilog)

    parser.add_argument(
                        "--jsonp",
                        help="JSONP file obtained from the rarefaction curve data",
                        required=True,
                        dest="jsonp"
                        )

    parser.add_argument(
                        "--out-prefix",
                        help="Name of the outfile where the data will be placed",
                        required=True,
                        dest="out_prefix"
                        )

    return parser.parse_args(args)

def load_jsonp(file):
    """
    Open the JSONP file
    Transform it into a JSON
    Load JSON into dict
    """
    with open(file, "r") as infile:
        infile = infile.read()
    infile = "{" + infile.split("{", 1)[1].split("}")[0] + "}"
    infile = json.loads(infile)
    
    return infile

def get_mean_data(in_dict):
    """
    From the dict, access the "data" part
    Get each category, calculate the mean for each one
    """
    mean_dict = dict()

    for item in in_dict["data"]:
        if item[0] not in mean_dict.keys():
            mean_dict[item[0]] = {}

        mean_dict[item[0]][item[1]] = mean(item[2:-1])

    return mean_dict

def generate_data_list(mean_dict):
    """
    Thanks https://www.geeksforgeeks.org/python-split-nested-list-into-two-lists/
    for the help!
    """
    rows = []
    header = []

    for key, depths_vals in mean_dict.items():
        depths, category_row = map(
                                list, 
                                zip(*[[depth,row] for depth,row in depths_vals.items()])
                                  )

        category_row.insert(0, key)
        depths.insert(0,"Group Name\Depths")

        # If list is empty, this will be false
        if bool(header) is True:
            if len(header) != len(depths):
                # This should never happen
                print("No cuadran las profundidades")
                sys.exit()

        header = depths
        rows.append(category_row)

    all_rows = [header] + rows
    
    return all_rows

def create_tsv(tsv_list, out_prefix):
    """
    Write nested list to CSV
    Change . with , for decimals
    """
    with open(f"{out_prefix}.tsv", "w") as outfile:
        for row in tsv_list:
            outfile.write("\t".join([str(item).replace(".",",") for item in row]))
            outfile.write("\n")
    
    return True

def main(args=None):
    """
    Full process:
        -Load JsonP
        -Parse JsonP
        -Get the mean for each iteration on each category
        -Prepare the data for a tsv file
        -Generate the tsv file as output
    """
    args = parse_args(args)
    data_dict = load_jsonp(args.jsonp)
    mean_dict = get_mean_data(data_dict)
    tsv_list = generate_data_list(mean_dict)
    create_tsv(tsv_list, args.out_prefix)

if __name__ == "__main__":
    sys.exit(main())
