#!/usr/bin/env python

import datetime
import subprocess
import logging
import os

logger=logging.getLogger()

NOW=datetime.datetime.now()

ffmpeg_options='''-thread_queue_size 512 -f v4l2 -input_format yuyv422 -i /dev/video1 \
  -thread_queue_size 512 -f v4l2 -input_format yuyv422 -i /dev/video0 \
  -thread_queue_size 512 -f pulse -ac 2 -i default \
  -map 0 -map 1 -map 2\
  -c:v:0 h264 \
  -c:v:1 h264 \
  -c:a:2 mp3 \
  {metadata} \
  output.mkv'''

class Metadata:
    def __init__(self, **kwargs):
        self.dmetadata = {"title": "",
                          "license": "cc-by-sa",
                          "copyright": "linux-gull.ch",
                          "language": "fr",
                          "year": NOW.year}
        self.dmetadata.update(kwargs)
    def get_largs(self) -> list :
        largs=[]
        for k in self.dmetadata:
            if self.dmetadata[k]:
                largs.append("-metadata")
                largs.append("{}='{}'".format(k,self.dmetadata[k]))
        return largs
    def get_cmd_options_str(self) -> str:
        return " ".join(self.get_largs())

description="""ceci est untest de description
multiligne"""

metadata=Metadata(title="test", date="today", description=description)
def run_ffmpeg(metadata, output):
    cmd="ffmpeg "+ffmpeg_options.format(metadata=metadata.get_largs())
    output=subprocess.call(cmd, shell=True)





def callback_err(line):
    print("-err "+line.decode())
def callback_out(line):
    print("-out "+line.decode())

import shlex
import subprocess
import select
def run_cmd_while_reading_sterr_stdout(cmd, callback_out, callback_err):
    p = subprocess.Popen(shlex.split(cmd),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = []
    stderr = []
    while True:
        reads = [p.stdout.fileno(), p.stderr.fileno()]
        ret = select.select(reads, [], [])
        for fd in ret[0]:
            if fd == p.stdout.fileno():
                read = p.stdout.readline()
                callback_out(read)
                stdout.append(read)
            if fd == p.stderr.fileno():
                read = p.stderr.readline()
                callback_err(read)
                stderr.append(read)
        if p.poll() != None:
            break
    return (stdout, stderr)

class FfmpegMgmt():
    def __init__(self, cmd:str):
        self.cmd=cmd
    def launch_it(self):
        self.process=subprocess.Popen(shlex(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    def kill_it(self):
        self.process.kill(

        os.kill

def fork_cmd(cmd):
    subprocess.Popen(shlex.cmd)

if "__main__" == __name__:
    cmd='''ffmpeg -thread_queue_size 512 -f v4l2 -input_format yuyv422 -i /dev/video1 \
       -thread_queue_size 512 -f v4l2 -input_format yuyv422 -i /dev/video0 \
       -thread_queue_size 512 -f pulse -ac 2 -i default \
       -map 0 -map 1 -map 2\
       -c:v:0 h264 \
       -c:v:1 h264 \
       -c:a:2 mp3 \
       -y \
       output.mkv'''

    run_cmd_while_reading_sterr_stdout(cmd, callback_out, callback_err)






