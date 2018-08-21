import csv, sys
input_fn = sys.argv[1]
output_fn = sys.argv[2]
cmd_list = list()
with open(input_fn,'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cmd = 'sh extract_relevant_gifs.sh {:s}'.format(row['uuid'])
        cmd_list.append(cmd)
        
with open(output_fn,'w') as f:
    for cmd in cmd_list:
        f.write(cmd + '\n')
