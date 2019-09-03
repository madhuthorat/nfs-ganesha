#!/usr/bin/env python

import sys, re
import os, os.path
import shutil
import subprocess

def main():
    subprocess.check_call("lttng create", shell=True)
    subprocess.check_call("lttng enable-event -u mdcache:mdc_lru_ref", shell=True)
    subprocess.check_call("lttng enable-event -u mdcache:mdc_lru_unref", shell=True)
    subprocess.check_call("lttng enable-event -u mdcache:mdc_lru_reap", shell=True)
    subprocess.check_call("lttng enable-event -u mdcache:mdc_lru_get", shell=True)
    subprocess.check_call("lttng enable-event -u mdcache:mdc_lru_insert", shell=True)
    subprocess.check_call("lttng enable-event -u mdcache:mdc_lru_remove", shell=True)
    subprocess.check_call("lttng enable-event -u mdcache:mdc_kill_entry", shell=True)
    subprocess.check_call("lttng enable-event -u mdcache:mdc_readdir_cb", shell=True)
    subprocess.check_call("lttng start", shell=True)

    # Create the NFS-Ganesha service file in /etc/systemd
    filename = "/usr/lib/systemd/system/nfs-ganesha.service"
    data = open(filename).read()
    data = data.replace("${NUMACTL}",
            "LD_PRELOAD=/usr/lib64/ganesha/libganesha_trace.so ${NUMACTL}",
            1)
    filename = "/etc/systemd/system/nfs-ganesha.service"
    modify_file(filename, data)
    subprocess.check_call("systemctl daemon-reload", shell=True)
    print("\nSuccessfully created user modified nfs-ganesha service unit file "
          "'/etc/systemd/system/nfs-ganesha.service'. Remove this file to undo "
          "the changes done by this script!")

# Modify the file with the given data atomically
def modify_file(filename, data):
    from tempfile import NamedTemporaryFile
    f = NamedTemporaryFile(dir=os.path.dirname(filename), delete=False)
    f.write(data)
    f.flush()
    os.fsync(f.fileno())

    # If filename exists, get its stats and apply them to the temp file
    try:
        stat = os.stat(filename)
        os.chown(f.name, stat.st_uid, stat.st_gid)
        os.chmod(f.name, stat.st_mode)
    except:
        pass

    os.rename(f.name, filename)

main()
