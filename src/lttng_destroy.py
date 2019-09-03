#!/usr/bin/env python

import sys, re
import os, os.path
import shutil
import subprocess

def main():
    subprocess.check_call("lttng destroy", shell=True)
    subprocess.check_call("rm -f /etc/systemd/system/nfs-ganesha.service", shell=True)

main()
