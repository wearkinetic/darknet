import pandas as pd
with open('mturk_output.csv','r') as f:
    df = pd.read_csv(f, index_col=False)

workers = list(set(df['WorkerId'].values))
worker_approval = dict()
for w in workers:
    df_w = df[df['WorkerId']==w]
    agree = 0
    total = 0
    for _,row in df_w.iterrows():
        df_assignment = df[df['HITId']==row['HITId']]
        for _,ass_row in df_assignment.iterrows():
            if ass_row['WorkerId']==w:
                continue
            if ass_row['Answer.categories'] == row['Answer.categories']:
                agree += 1
            total += 1
    score = float(agree) / float(total)
    if score >= 0.8:
        worker_approval[w] = True
    else:
        worker_approval[w] = False
        print('Warning, worker {:s} rejected'.format(w))
        print('Score = ', score)

count = 0
total = 1
for v in worker_approval.itervalues():
    if not v:
        count += 1
    total += 1

print('rejected {:d} of {:d} workers'.format(count,total))

#Now start editing the csv.
field_names = list(df.columns)
with open('mturk_output.csv','r') as f_in:
    import csv
    reader = csv.DictReader(f_in)
    with open('mturk_output_moderated.csv','w') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=field_names)
        writer.writeheader()
        for row in reader:
            w = row['WorkerId']
            if worker_approval[w]:
                row['Approve'] = 'x'
            else:
                row['Reject'] = 'large discrepency with other workers'
            writer.writerow(row)
