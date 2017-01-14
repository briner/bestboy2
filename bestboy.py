#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import shlex
import signal
import datetime
import re
import argparse
# pip
from hurry.filesize import size, alternative
#
import bestboy_cfg

MKV="output.mkv"
RE_DURATION=re.compile("^DURATION\s+:\s+(\d{2}):(\d{2}):(\d{2})\.\d+$")


def preexec_function():
    os.setpgrp()

class ConsoleLine:
    def __init__(self):
        self.len=0
    def write(self, string):
        sys.stdout.write(string)
        sys.stdout.flush()
        self.len+=len(string)
    def erase(self):
        if self.len>0:
            sys.stdout.write("\b \b"*self.len)
        sys.stdout.flush()
        self.len=0
    def newline(self):
        if self.len:
            sys.stdout.write(os.linesep)
            sys.stdout.flush()
        self.len=0
console_line=ConsoleLine()

def seems_a_important_movie(filepath):
    lline=subprocess.check_output(shlex.split("/usr/bin/mediainfo "+filepath)).decode().splitlines()
    duration_t=[0,0,0]
    for line in lline:
        match=RE_DURATION.search(line)
        if match:
            duration_t=[int(e) for e in RE_DURATION.search(line).groups()]
            break
    #
    if datetime.timedelta(0,5,0) < datetime.timedelta(*duration_t):
        return True
    return False


#
# def manage_movie(filepath) -> str:
#     if not os.path.isfile(filepath):
#         return filepath
#     if not seems_a_important_movie(filepath):
#
#
#             pass
#         else:


def main(cmd_fmt, filepath):
    start=datetime.datetime.now()
    tmpmovpath="tmp_{}_{}.avi".format(filepath, start.strftime("%Hh%Mm%Ss"))
    tmplogpath="tmp_{}_{}.log".format(filepath, start.strftime("%Hh%Mm%Ss"))
    cmd_inst=cmd_fmt.format(filename=tmpmovpath)
    print("Launch it with cmd:")
    print(" " + cmd_inst)
    #
    fh_log=open(tmplogpath,"w")
    process=subprocess.Popen(shlex.split(cmd_inst),
                             stdin=subprocess.PIPE,
                             stdout=fh_log,
                             stderr=fh_log,
                             preexec_fn=preexec_function)

    def signal_handler(asignal, frame):
        console_line.newline()
        print('You pressed Ctrl+C!')
        stop_it=input("Do you want to stop this record [y/N]")
        if stop_it.lower()=="y":
            print(process.pid)
            process.send_signal(signal.SIGINT)
            sys.exit(0)
        else:
            print("keep it")

    signal.signal(signal.SIGINT, signal_handler)

    #
    state="not_started"
    while True:
        # TODO:    /dev/video1: Device or resource busy
        if not os.path.isfile(MKV):
            if state=="not_started":
                print("file ({}) not yet created !".format(MKV))
                state="started"
            time.sleep(1)
            continue
        now=datetime.datetime.now()
        now_str=now.strftime("%Hh%Mm%Ss")
        delta_str=".".join(str(now-start).split(".")[:-1])
        size_si_str=size(os.path.getsize(MKV), system=alternative)
        now_str=datetime.datetime.now().strftime("%Hh%Mm%Ss")
        msg="@{} size : {:>6}, duration: {}".format(now_str, size_si_str, delta_str)
        console_line.erase()
        console_line.write(msg)
        time.sleep(1)

if "__main__" == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", default="test.mkv")
    args = parser.parse_args()

    config=bestboy_cfg.config[bestboy_cfg.default_configname]
    main(config.cmd_fmt, args.filepath)
