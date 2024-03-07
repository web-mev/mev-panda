// a few hardcoded values:
params.motif_files_map = [
    symbol: "s3://webmev-public/tissues_motif.symbol.tsv",
    ensembl: "s3://webmev-public/tissues_motif.ensg.tsv"
]
params.ppi_file = "s3://webmev-public/tissues_ppi.tsv"

// maximum number of genes to keep so we don't blow up the memory
params.nmax = 25000 

process run_panda {
    tag "Run panda"
    publishDir "${params.output_dir}/MevPanda.panda_output_matrix", mode:"copy", pattern:"${output_name}"
    container "ghcr.io/web-mev/mev-panda"
    cpus 16
    memory '120 GB'

    input:
        path exprs_file
        path motif_file
        path ppi_file

    output:
        path "${output_name}"

    script:
        output_name = "panda_network.tsv"
        """
        python3 /usr/local/bin/panda.py \
            --motif ${motif_file} \
            --ppi ${ppi_file} \
            --output ${output_name} \
            --nmax ${params.nmax} \
            ${exprs_file}
        """
}

workflow {

    ppi_file_ch = Channel.fromPath(params.ppi_file)
    motif_file_ch = Channel.fromPath(params.motif_files_map[params.identifier_choice.toLowerCase()])
    run_panda(params.exprs_file, motif_file_ch, ppi_file_ch)
}
