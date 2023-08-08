R1=snakemake.input.R1
counts_file=open(snakemake.output.counts, 'w')

def revcom(seq,nuc='DNA'):
	if nuc=='DNA':
		complement={'N':'N','A':'T','C':'G','G':'C','T':'A','a':'t','t':'a','c':'g','g':'c', 'U':'A', 'u':'a', '-':'-'}
	else:
		complement={'N':'N','A':'U','C':'G','G':'C','U':'A','a':'u','u':'a','c':'g','g':'c','-':'-'}
	return ''.join(reversed([complement[base] for base in seq]))

def get_barcode_counts(sample_dict):
	'''
	gets a distribution of barcode counts for each fasta file associated with a
	sample, and prints this alongside what the barcodes were supposed to be
	'''
	import gzip
	final_dict={}
	for line_number, line in enumerate(gzip.open(R1, mode='rt')):
		if line_number%4==0:
			barcodes=tuple(line.strip().split(' ')[-1].split(':')[-1].split('+'))
			edited_barcodes=[revcom(barcodes[1]), revcom(barcodes[0])]
			if edited_barcodes not in final_dict:
				final_dict[edited_barcodes]=0
			final_dict[edited_barcodes]+=1
	return final_dict

def output_counts(final_dict):
	count_file.write('forward_barcode', 'reverse_barcode', count)
	for barcodes in final_dict:
		forward, reverse=barcodes
		count_file.write(f'{forward}\t{reverse}\t{final_dict[barcodes]}\n')
