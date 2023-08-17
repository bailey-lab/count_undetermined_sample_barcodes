# Count Undetermined Sample Barcodes

Given an 'Undetermined' fastq file (or several undetermined fastq files), this
program tells the user how many barcodes of each type were present in each file.

## Installation:
Install conda (if you don't already have it, or if you'd like a better conda)
with:
[https://github.com/conda-forge/miniforge#mambaforge](https://github.com/conda-forge/miniforge#unix-like-platforms-mac-os--linux)

This link will install a version of conda called 'mamba' that also includes
conda. mamba runs faster than conda, results in fewer ambiguities when resolving
packages, and is easier to install on a per-user basis. For best results with
this pipeline, use mamba. Don't forget to read the instructions at the end of
the setup script regarding logging out and back in.

Install snakemake in an environment called snakemake with:
```bash
mamba create -c conda-forge -c bioconda -n snakemake snakemake
```

or (if you didn't install mamba) with

Install snakemake in an environment called snakemake with:
```bash
conda create -c conda-forge -c bioconda -n snakemake snakemake
```

## Usage:
 - Download the contents of this git repo to a folder on your machine and cd
 into that folder (so that "ls" shows setup_run.smk and finish_run.smk).
 - Open the count_undetermined_barcodes.yaml file and fill in the variables using
instructions from the comments
 - Activate snakemake with:
```bash
mamba activate snakemake
```
 - Run the first step with:
```bash
snakemake -s count_undetermined_barcodes.smk --cores 10
```

## not yet implemented:
In the future, if a user provides sample sheet and barcode labeling file, this
program also will tell the user what barcodes and what samples the undetermined
barcodes might map to.
