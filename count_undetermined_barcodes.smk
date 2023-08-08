configfile: 'count_undetermined_barcodes.yaml'
input_folder=config['input_folder']
output_folder=config['output_folder']
read1=config['R1']
suffix=config['suffix']

rule all:
	input:
		yaml_file=output_folder+'/snakemake_params/count_undetermined_barcodes.yaml',
		counts=expand(output_folder+'/counts/{sample}_barcode_counts.tsv', sample=config['samples'])

rule copy_files:
	input:
		snakemake_file='count_undetermined_barcodes.smk',
		yaml_file='count_undetermined_barcodes.yaml',
		scripts='scripts'
	output:
		snakemake_file=output_folder+'/snakemake_params/count_undetermined_barcodes.smk',
		yaml_file=output_folder+'/snakemake_params/count_undetermined_barcodes.yaml',
		scripts=directory(output_folder+'/snakemake_params/scripts')
	shell:
		'''
		cp {input.snakemake_file} {output.snakemake_file}
		cp {input.yaml_file} {output.yaml_file}
		cp -r {input.scripts} {output.scripts}
		'''

rule count_undetermined:
	'''
	Returns what barcodes are present and what their abundances are in any given
	sample. read1 and read2 have identical barcodes, so only need to count
	barcode counts on read1 files
	'''
	input:
		R1=input_folder+'/{sample}_'+read1+'_'+suffix,
	output:
		counts=output_folder+'/counts/{sample}_barcode_counts.tsv'
	script:
		'scripts/count_undetermined.py'

