# /usr/bin/env python

import argparse
from netZooPy.panda import Panda
import pandas as pd
import pickle
import sys


def run_panda(args, panda_output):
    '''
    Runs PANDA object creation and exports output to file and pickle.
    '''
    # Load the data as a pandas dataframes
    exprs_df = pd.read_csv(args.exprs, index_col = 0, header = 0, sep = "\t")
    motif_df = pd.read_csv(args.motif, header = None, sep = "\t")
    ppi_df = pd.read_csv(args.ppi, header = None, sep = "\t")
    # Adding headers for the PANDAs obj to read
    motif_df.columns =['source','target','weight']
    # Running pandas with default expected paramaters
    # save_memory = False results in outputting the PANDA network in edge format
    # save_memory = True results in a matrix format
    # Edge format results in massive memory usage after PANDA finishes
    # LIONESS requires keep_expression_matrix
    # Default modeProcess blows memory stack, so have to use "legacy".
    # Pass the pandas dataframes directly rather than the PATHs.
    panda_obj = Panda(
        exprs_df,
        motif_df,
        ppi_df,
        remove_missing = False, 
        keep_expression_matrix = True, 
        save_memory = False,
        modeProcess = "legacy"
    )
    # Pull PANDA network out of object
    out_mtx = pd.DataFrame(panda_obj.panda_network)

    # Get motif order
    motif_names_ordered = motif_df[0].drop_duplicates(keep="first")
    # Set headers and rownames to PANDA network
    out_mtx.set_index(motif_names_ordered, inplace=True)
    out_mtx.columns = exprs_df.index.values
    out_mtx.transpose().to_csv(
        panda_output,
        sep = "\t",
        header = True,
        index = True
    )


def main():
    # Parse args
    parser = argparse.ArgumentParser(
        desc="Runs PANDA on input count matrix."
    )
    parser.add_argument(
        "--ranges", metavar="INT", required=True,
        help="Number of slice ranges"
    )
    parser.add_argument(
        "--motif", metavar="TSV", required=True,
        help="Motif data"
    )
    parser.add_argument(
        "--ppi", metavar="TSV", required=True,
        help="PPI data"
    )
    parser.add_argument(
        "exprs", metavar="TSV",
        help="Expression count matrix"
    )
    args = parser.parse_args()
    panda_output = "panda_output.mtx" # Temporary name
    # Run PANDA
    run_panda(args, panda_output)


if __name__ == "__main__":
    main()
