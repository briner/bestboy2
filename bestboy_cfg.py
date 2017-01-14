class BestboyConfig():
    cmd_fmt='''ffmpeg -thread_queue_size 512 -f v4l2 -input_format h264    -framerate 24 -video_size 800x600   -i /dev/video1
                  -thread_queue_size 512     -f v4l2 -input_format yuyv422 -framerate 24                       -i /dev/video0
                  -thread_queue_size 512 -f pulse -ac 2 -i default
                  -map 0 -map 1 -map 2
                  -c:v:0 copy
                  -c:v:1 h264
                  -c:a:2 mp3
                  -y
                  {filename}'''

default_configname="default"
default_filename="test"
config={"default": BestboyConfig()}