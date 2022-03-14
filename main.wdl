workflow MevPanda {

    # A motif file. Since this is optional, we provide
    # a default 'value'. This is b/c of how WDL handles
    # optional args in the command section (it doesn't)
    File? motif_file = "__motif__"

    # A PPI file. Optional. same as above
    File? ppi_file = "__ppi__"

    # A user uploaded exprs count matrix
    File exprs_file

    String output_name_prefix = "panda_matrix_results"

    call runPanda {
        input:
            motif_file = motif_file,
            ppi_file = ppi_file,
            exprs_file = exprs_file
    }

    output {
        File panda_output_matrix = runPanda.panda_output_matrix
    }
}

task runPanda {
    File motif_file
    File ppi_file
    File exprs_file

    String output_name = "panda_network.tsv"
    Int disk_size = 40

    command {
        python3 /opt/software/panda.py \
            --motif ${motif_file} \
            --ppi ${ppi_file} \
            --output ${output_name}
            ${exprs_file}
    }

    output {
        File panda_output_matrix = ${output_name}
    }

    runtime {
        docker: "ghcr.io/web-mev/mev-panda"
        cpu: 8
        memory: "62 G"
        disks: "local-disk " + disk_size + " HDD"
        preemptible: 0
    }
}