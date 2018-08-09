UUID=$1

# download video
echo "Downloading video"
mkdir -p $UUID
aws s3 cp s3://kinetic-forensic-videos/$UUID $UUID/video.mp4

# extract frames
echo "Extracting Frames"
mkdir -p $UUID/frames
ffmpeg -i $UUID/video.mp4 -q:v 10 $UUID/frames/frame_%d.jpg -hide_banner

# run yolonet
echo "Running yolo-net"
ls $UUID/frames/ > $UUID/yolo_input.txt
sed -i -e "s/frame_/$UUID\/frames\/frame_/" $UUID/yolo_input.txt
./darknet detector test ./cfg/coco.data ./cfg/yolov3.cfg ./yolov3.weights < $UUID/yolo_input.txt > $UUID/yolo_output.txt

# parse the output
echo "Parsing yolo output"
python parse_yolo_output.py $UUID/yolo_output.txt

# create gifs (uploaded to s3://mturk/$(UUID)/frame_X_through_Y.gif)
echo "Creating gifs"
python create_gifs.py $UUID/time_windows.json
