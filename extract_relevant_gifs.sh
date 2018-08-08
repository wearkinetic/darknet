UUID=$1

# download video
aws s3 cp s3://kinetic-forensic-videos/$UUID $UUID/video.mp4

# extract frames
mkdir -p $UUID/frames
ffmpeg -i $UUID/video.mp4 -q:v 10 $UUID/frames/frame_%d.jpg -hide_banner

# run yolonet
./darknet detector test ./cfg/coco.data ./cfg/yolov3.cfg ./yolov3.weights -dont_show < data/train.txt > $UUID/yolo_output.txt

# parse the output
python parse_yolo_output.py $UUID/yolo_output.txt

# create gifs (uploaded to s3://mturk/$(UUID)/frame_X_through_Y.gif)
python create_gifs.py $UUID
