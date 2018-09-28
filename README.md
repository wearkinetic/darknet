# Mechanical_twerk #
Mechanical twerk is a collection of scripts for using Amazon Mechanical Turk to annotate the actions of videos in scarif.
![twerkerama](http://cdn.smosh.com/wp-content/uploads/ftpuploads/bloguploads/0913/nerdy-twerking-futurama.gif)

## Setup ##
At least part of the pipeline should be run on an ec2 instance of the `Deep Learning AMI (Amazon Linux) Version 9.0 (ami-5f2fa120)`. I reccomend cloning this repository both locally and in an ec2 instance. After initializing your instance you must
  1. run `make`
  2. download the yolov3 weights `wget https://pjreddie.com/media/files/yolov3.weights`
  2. `source activate tensorflow_p36` to activate the Conda Environment
  3. `aws configure` (get credentials from somebody)
  4. `sudo yum install ImageMagick` (after a `sudo yum update`)

## Usage ##
Here is the overall sequence
  1. Create gifs and post them to s3 (do this on a Deep Learning AMI)
  2. Create a csv of gif-urls
  3. Go to https://requester.mturk.com/ and create a new batch job (upload this csv)
  4. Once the jobs are completed, download the results and parse them
    a. Run a sanity check (optional)
  5. Run the annotate script to post the annotations to scarif.

### Create gifs ###
For a single scarif video uuid you may run
```shell
> sh extract_relevant_gifs.sh $UUID
```
This script downloads the video, runs yolonet, parses the result, creates gifs, and uploads them to s3 at `s3://mturk/$UUID/frame_X_though_Y.gif` where `X` and `Y` are frame indices indicating the range of frames included in the given gif.

For batch processing do
```shell
> python batch_extract_relevant_gifs.py PATH/TO/FILE/OF/UUIDS
```
where the file of uuids is a text file where each line is a uuid.
In this case we expect each of the uuids to be associated to a video of the same
annotation category.  Here are the possible categories:
 - squat lifts
 - twisting
 - bad lifts
 - ladder climbing
 - ladder jumping
 - safe jumping


### Create csv of gif-urls ###
For a single scarif-video UUID, you can create a csv file containing presigned urls to gifs created in the previous step using
```shell
> python generate_presigned_url_table.py $UUID
```

For a batch of uuids do
```shell
> python batch_generate_presigned_urls.py
```
where the file of uuids is a text file where each line is a uuid.


The csv is written to `$[NAME_OF_INPUT_FILE]_urls.csv`. The urls last about a day.

### Create a new batch job ###
You to use the HIT Type and Layout corresponding to the contents of the video. For example, there is one layout just for videos that involve people on ladders, another layout for videos of people doing bad bends.
These layouts are currently associated with the tech@wearkinetic.com account at  [https://requester.mturk.com/](https://requester.mturk.com/). I recommend visiting [https://requester.mturk.com/](https://requester.mturk.com/), getting confused, and then reading the documentation for creating a batch job on AMT  [here](https://console.aws.amazon.com/console/home). In one step, you are asked to upload a csv.  That is where you upload the file created in the previous step. We might be able to automate this and avoid using the GUI, but it's probably not worth the time.

### Parse the AMT results ###
After you approve the results on AMT, you can download them as a csv-file and then run
```shell
> source .scarif_creds
> python parse_mturk_output.py AMT_RESULT.csv
```
where `.scarif_creds` is a file of the form
```
export SCARIF_HOST=terraform-003403234NumbersAreCool.sdlfkjRandomness.us-east-2.rds.amazonaws.com
export SCARIF_PASS=TheBestPasswordEver
export SCARIF_USER=JohnMalkovich
```

**CAUTION: THIS POSTS THE ANNOTATIONS TO SCARIF** (idempotently)

Hooray!  You are done.

## Extra: Automating The Mturk Requester step
In the future, if this step is automated the following table will probably be useful

| video contents | HIT Type ID | Layout ID |
| --- | --- | --- |
| squat lifts | `3RSP1MSSW0L7M90318VNFEAIM3NUK4` | `346UV3PWV7FPWMS6JOOM1WARLDBNEG` |
| twisting | `3RSP1MSSW0L7M90318VNFEAIM3NUK4` | `3GK1B7C7NNLX16GQQ4TLZV12OAM2NU` |
| bad lifts | `3RSP1MSSW0L7M90318VNFEAIM3NUK4` | `3LQR9N58ZMFJWAT3QGLM3MB2R65KDF` |
| ladder climbing | `385XUCFVXXPMLM00L6IC4JN53O14V8` | `3FVQ71UKJAYXER6C7CK1V7YIYU5YLT` |
| ladder jumping | `36NY760EF7GMUCJQGBMTT21SMWVB3U` | `375TY3MH0W6WZWTV0C7X6K6FWQ2KJT` |
| safe jumping | `3O471962EPEC5TWDC2PJFIOO5322UR` | `3U3GGGLICJMAZO8SNXIRB8AO01ZCND` |


## Darknet
This repo was originally forked from [Darknet](https://github.com/pjreddie/darknet), an open source neural network framework written in C and CUDA. It is fast, easy to install, and supports CPU and GPU computation.

For more information see the [Darknet project website](http://pjreddie.com/darknet).

For questions or issues please use the [Google Group](https://groups.google.com/forum/#!forum/darknet).
