workflow mevPanda {
    # A fixed motif file
    File motif_file
    # A fixed PPI file
    File ppi_file
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

    Int disk_size = 40

    command {
        python3 /opt/software/panda.py \
            --motif ${motif_file} \
            --ppi ${ppi_file} \
            ${exprs_file};
    }

    output {
        File panda_output_matrix = glob("${output_name_prefix}*")[0] # This likely needs fixing.
    }

    runtime {
        docker: "hsphqbrc/mev-netzoopy"
        cpu: 8
        memory: "128 G"
        disks: "local-disk " + disk_size + " HDD"
        preemptible: 0
    }
}