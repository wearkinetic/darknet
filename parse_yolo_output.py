import sys, os
yolo_output_fn = sys.argv[1]
uuid,_ = os.path.split(yolo_output_fn)

def parse(lines):
    output = dict()
    for line in lines:
        strings = line.split(': ')
        if strings[0] == 'Enter Image Path':
            current_frame = strings[1]
            if current_frame != "":
                output[current_frame] = 0
        if strings[0] == 'person':
            confidence = int(strings[1].strip('%\n'))
            output[current_frame] = confidence
    return output

with open(yolo_output_fn,'r') as f:
    output = parse(f.readlines())

import re
N_frames = len(output)
confidences = [0]*N_frames
for k,v in output.items():
    _,fn = os.path.split(k)
    if fn[:5] == "frame":
        try:
            frame_idx = int(re.findall(r'\d+',fn)[0])
        except:
            print("failed to extract an index from {:s}".format(fn))
            continue
        confidences[frame_idx-1] = v

windows = []
for i in range(0, len(confidences), 15):
    count = sum([1 for x in confidences[i:i+29] if x > 95])
    if count > 15:
        windows.append([i+1,i+30]) #the files use 1 based indexing

with open('{:s}/time_windows.json'.format(uuid),'w') as f:
    import json
    json.dump(windows,f)
