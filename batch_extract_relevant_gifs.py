import sys
from subprocess import run, PIPE
with open(sys.argv[1],'r') as f:
    for uuid in f.readlines():
        uuid = uuid.strip('\n')
        cmd = 'sh extract_relevant_gifs.sh {:s}'.format(uuid)
        completed_process = run(cmd,shell=True, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        with open('logs/{:s}.log'.format(uuid),'w') as flog:
            flog.write(completed_process.stderr)
        with open('logs/{:s}.out'.format(uuid),'w') as fout:
            fout.write(completed_process.stdout)
        print('completed processing of {:s}'.format(uuid))
