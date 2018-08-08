# Mechanical_twerk #
Mechanical twerk is a collection of scripts for using Amazon Mechanical Turk to annotate the actions of videos in scarif.
![twerkerama](http://cdn.smosh.com/wp-content/uploads/ftpuploads/bloguploads/0913/nerdy-twerking-futurama.gif)

## Setup ##
This is intended to be run on an ec2 instance of the `Deep Learning AMI (Amazon Linux) Version 9.0 (ami-5f2fa120)`.
After initializing your instance you must
  1. run `make`
  2. download the yolov3 weights `wget https://pjreddie.com/media/files/yolov3.weights`
  2. `source activate tensorflow_p36` to activate the Conda Environment
  3. `aws configure` (get credentials from somebody)
  4. `sudo apt-get install imagemagick`

## Usage ##
Here is the overall sequence
  1. Create gifs and post them to s3
  2. Create a csv of gif-urls
  3. Go to https://requester.mturk.com/ and create a new batch job (upload this csv)
  4. Once the jobs are completed, download the results and parse them
    a. Run a sanity check (optional)
  5. Run the annotate script to post the annotations to scarif.

### Create gifs ###
For a single scarif video uuid you may run
```shell
> extract_relevant_gifs.sh $UUID
```
This script downloads the video, runs yolonet, parses the result, creates gifs, and uploads them to s3 at `s3://mturk/$UUID/frame_X_though_Y.gif` where `X` and `Y` are frame indices indicating the range of frames included in the given gif.

### Create csv of gif-urls ###
Again, for a single scarif-video UUID, you can create a csv file containing presigned urls to gifs created in the previous step using
```shell
> python generate_presigned_url_table.py $UUID -hours=5
```
The `hours` option determines the expiration time of the urls. The csv is written to `$UUID_urls.csv`

### Create a new batch job ###
This is all GUI work. Details to follow.

### Parse the AMT results ###
Simply run
```shell
> python parse_AMT_result.py AMT_RESULT.csv
```
The output will be written to `$(UUID)_proposed_annotations.json`. If you would also like to sanity check the result you can include the option `-sanity_check` to create videos.

### Post annotations to scarif ###
Run
```shell
> python post_annotations.py $(UUID)_proposed_annotations.json
```

# Darknet #
This repo was originally forked from [Darknet](https://github.com/pjreddie/darknet), an open source neural network framework written in C and CUDA. It is fast, easy to install, and supports CPU and GPU computation.

For more information see the [Darknet project website](http://pjreddie.com/darknet).

For questions or issues please use the [Google Group](https://groups.google.com/forum/#!forum/darknet).
