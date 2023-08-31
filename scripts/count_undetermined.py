R1=snakemake.input.R1
print('R1 is', R1)
real_barcodes=snakemake.input.real_barcodes
counts_file=open(snakemake.output.counts, 'w')
threshold=snakemake.params.threshold

known_barcode_dict={}
for line in open(real_barcodes):
	line=line.strip().split('\t')
	barcode, barcode_number=line[4], line[5]
	known_barcode_dict[barcode]=barcode_number

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

def get_barcode_status(barcode):
	if barcode in known_barcode_dict:
		barcode_status=known_barcode_dict[barcode]
	else:
		barcode_status='not a valid barcode'
	return barcode_status

def output_counts(final_dict):
	counts_file.write('forward_barcode\treverse_barcode\tforward_barcode_number\treverse_barcode_number\tcount\n')
	unsorted_list=[]
	for barcodes in final_dict:
		if final_dict[barcodes]>threshold:
			forward, reverse=barcodes
			count=final_dict[barcodes]
			forward_status=get_barcode_status(forward)
			reverse_status=get_barcode_status(reverse)
			unsorted_list.append([count, forward, reverse, forward_status, reverse_status])
	sorted_list=sorted(unsorted_list, reverse=True)
	for entry in sorted_list:
		counts_file.write(f'{entry[1]}\t{entry[2]}\t{entry[3]}\t{entry[4]}\t{entry[0]}\n')
final_dict=get_barcode_counts()
output_counts(final_dict)
