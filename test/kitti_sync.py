#! /usr/bin/env python

# For Py2/3 compatibility
from __future__ import (absolute_import, division, print_function, unicode_literals)
#from builtins import *

import sys
import os

def locateUnsyncedFiles(timestamp_raw_filepath, timestamp_sync_filepath):
    with open(timestamp_raw_filepath, 'r') as ts_raw_f, open(timestamp_sync_filepath, 'r') as ts_sync_f:
        count = -1
        removeFiles = list()
        synced = ts_sync_f.readline().split()[-1]
#        print(synced)
        syncReadNew = False
        syncEnd = False
        syncReads = 1

        for rawLine in ts_raw_f:

            raw = rawLine.split()[-1]
            count += 1

            if syncReadNew and (not syncEnd):
                syncLine = ts_sync_f.readline()

                if syncLine == "":
                    syncEnd = True
                else:
#                    print("Line read:", syncLine)
                    synced = syncLine.split()[-1]
                    syncReads += 1
#                    print("Read count of synced file:", syncReads)
                    syncReadNew = False

            if raw == synced:
                syncReadNew = True
#                print(count)
            else:
                removeFiles.append(str(count).zfill(10) + '.png')

        print("Files to be removed: ", removeFiles)
        return removeFiles

def main():
    datadir = sys.argv[1]
    drive = sys.argv[2]

    datadir_raw = datadir + "_drive_" + drive + "_extract"
    datadir_sync = datadir + "_drive_" + drive + "_sync"
    datadir_rawsync = datadir + "_drive_" + drive + "_rawsync"

    dirsToSync = ("image_00", "image_01", "image_02", "image_03")

    for directory in dirsToSync:
        timestamp_raw_filepath = 
        timestamp_sync_filepath = 

        removeFiles = locateUnsyncedFiles(timestamp_raw_filepath, timestamp_sync_filepath)
    


if __name__ == "__main__":
    main()

