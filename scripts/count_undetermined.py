R1=snakemake.input.R1
print('R1 is', R1)
counts_file=open(snakemake.output.counts, 'w')
threshold=snakemake.params.threshold

def revcom(seq,nuc='DNA'):
	if nuc=='DNA':
		complement={'N':'N','A':'T','C':'G','G':'C','T':'A','a':'t','t':'a','c':'g','g':'c', 'U':'A', 'u':'a', '-':'-'}
	else:
		complement={'N':'N','A':'U','C':'G','G':'C','U':'A','a':'u','u':'a','c':'g','g':'c','-':'-'}
	return ''.join(reversed([complement[base] for base in seq]))

def get_barcode_counts():
	'''
	gets a distribution of barcode counts for each fasta file associated with a
	sample, and prints this alongside what the barcodes were supposed to be
	'''
	import gzip
	final_dict={}
	for line_number, line in enumerate(gzip.open(R1, mode='rt')):
		if line_number%4==0:
			barcodes=tuple(line.strip().split(' ')[-1].split(':')[-1].split('+'))
			edited_barcodes=tuple([revcom(barcodes[1]), revcom(barcodes[0])])
			if edited_barcodes not in final_dict:
				final_dict[edited_barcodes]=0
			final_dict[edited_barcodes]+=1
	return final_dict

def output_counts(final_dict):
	counts_file.write('forward_barcode\treverse_barcode\tcount\n')
	unsorted_list=[]
	for barcodes in final_dict:
		if final_dict[barcodes]>threshold:
			forward, reverse=barcodes
			count=final_dict[barcodes]
			unsorted_list.append([count, forward, reverse])
	sorted_list=sorted(unsorted_list, reverse=True)
	for entry in sorted_list:
		counts_file.write(f'{entry[1]}\t{entry[2]}\t{entry[0]}\n')

final_dict=get_barcode_counts()
output_counts(final_dict)
