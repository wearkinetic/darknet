import sys, os, boto3
windows_fn = sys.argv[1]
uuid,_ = os.path.split(windows_fn)
with open(windows_fn,'r') as f:
    import json
    windows = json.load(f)

from subprocess import Popen
gif_dir = '{:s}/gifs'.format(uuid)
s3 = boto3.client('s3')
if not os.path.isdir(gif_dir):
    os.makedirs(gif_dir)

commands = list()
files = list()
for start, end in windows:
    fn = '{:s}/frame_{:d}_to_{:d}.gif'.format(gif_dir,start,end)
    if os.path.isfile(fn):
        continue
    cmd = 'convert -resize 10% -delay 10 -loop 0 \
{:s}/frames/frame_{{{:d}..{:d}}}.jpg {:s}'.format(uuid,start,end,fn)
    commands.append(cmd)
    files.append(fn)

# run in parallel
processes = [Popen(cmd, shell=True) for cmd in commands]

# wait for completion
keys = list()
for p,fn in zip(processes,files):
    try:
        return_code = p.wait()
    except:
        continue
    if return_code != 0:
        print('failed to create {:s}'.format(fn), file=sys.stderr)
    else:
        try:
            s3.upload_file(Bucket='kinetic-mechanical-twerk', Key=fn, Filename=fn)
            keys.append(fn)
        except:
            print('failed to upload {:s}'.format(fn), file=sys.stderr)

with open('{:s}/gif_keys.json', 'w') as f:
    import json
    json.dump(keys,f)
