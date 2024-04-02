import sys
import argparse
from netZooPy.panda import Panda
import pandas as pd


def run_panda(args):
    '''
    Runs PANDA object creation and exports output to file.
    '''
    # Load the data as a pandas dataframes
    exprs_df = pd.read_csv(args.exprs, index_col=0, header=0, sep="\t")
    motif_df = pd.read_csv(args.motif, header=None, sep="\t")
    ppi_df = pd.read_csv(args.ppi, header=None, sep="\t")

    # Adding headers for the PANDAs obj to read
    motif_df.columns = ['source', 'target', 'weight']

    # subset the expression dataframe to retain only the top NMAX
    # by mean expression. Otherwise, memory consumption is too much.

    # covering a very fringe case here where this column might
    # already be in the matrix. Just keep adding underscores to
    # create a unique column name for the row-mean values.
    mean_col_name = '__mean__'
    while mean_col_name in exprs_df.columns:
        mean_col_name = '_' + mean_col_name + '_'
    exprs_df[mean_col_name] = exprs_df.apply(lambda x: x.mean(), axis=1)

    # retain only the top NMAX and drop that mean value column
    # since we're done with it.
    exprs_df = exprs_df.nlargest(args.nmax, mean_col_name)
    exprs_df.drop(mean_col_name, axis=1, inplace=True)

    # Running pandas with default expected paramaters
    # save_memory = False results in outputting the PANDA network
    # in edge format
    # save_memory = True results in a matrix format
    # Edge format results in massive memory usage after PANDA finishes
    # LIONESS requires keep_expression_matrix
    # Default modeProcess blows memory stack, so have to use "legacy".
    # Pass the pandas dataframes directly rather than the PATHs.
    try:
        panda_obj = Panda(
            exprs_df,
            motif_df,
            ppi_df,
            remove_missing=False,
            keep_expression_matrix=True,
            save_memory=False,
            modeProcess="legacy"
        )
    except Exception as ex:
        sys.stdout.write(f'Error" {ex}')

    # Pull PANDA network out of object
    out_mtx = pd.DataFrame(panda_obj.panda_network)

    # Get motif order
    motif_names_ordered = motif_df['source'].drop_duplicates(keep="first")
    # Set headers and rownames to PANDA network
    out_mtx.set_index(motif_names_ordered, inplace=True)
    out_mtx.columns = exprs_df.index.values
    out_mtx.transpose().to_csv(
        args.output,
        sep="\t",
        header=True,
        index=True
    )


def main():
    parser = argparse.ArgumentParser(
        description="Runs PANDA on input count matrix."
    )

    parser.add_argument(
        "--motif",
        metavar="TSV",
        required=True,
        help="Motif data"
    )

    parser.add_argument(
        "--ppi",
        metavar="TSV",
        required=True,
        help="PPI data"
    )

    parser.add_argument(
        "--nmax",
        type=int,
        metavar="INT",
        required=False,
        default=25000,
        help="Max number of genes to consider. We take the top N by row-mean."
    )

    parser.add_argument(
        '--output',
        required=True,
        help='The name of the output file.'
    )

    parser.add_argument(
        "exprs",
        metavar="TSV",
        help="Expression count matrix"
    )

    args = parser.parse_args()

    run_panda(args)


if __name__ == "__main__":
    main()
