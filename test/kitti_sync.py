#! /usr/bin/env python

# For Py2/3 compatibility
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

import sys
import os
import shutil

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

        return removeFiles

def removeUnsyncedFilesAndSync(rawsync_dirToSync_path, removeFiles):
    imageDataDir = os.path.join(rawsync_dirToSync_path, 'data')

    for fname in removeFiles:
        os.remove(os.path.join(imageDataDir, fname))

    count = 0

    # Read names of files in imageDataDir, sort them and rename them
    imageFileList = os.listdir(imageDataDir)
    imageFileList.sort()

    for oldName in imageFileList:
        newName = str(count).zfill(10) + '.png'
        os.rename(os.path.join(imageDataDir, oldName), os.path.join(imageDataDir, newName))
        count += 1

def main():
    datadir = sys.argv[1]
    drive = sys.argv[2]

    if not os.path.isdir(datadir):
        # Raise an error and exit the program
        sys.exit("Directory " + datadir + " does not exist")

    datadir_basename = os.path.basename(datadir)
    datadir_raw = datadir_basename + "_drive_" + drive + "_extract"
    datadir_sync = datadir_basename + "_drive_" + drive + "_sync"
    datadir_rawsync = datadir_basename + "_drive_" + drive + "_rawsync"

    datadir_raw_path = os.path.join(datadir, datadir_raw)
    datadir_sync_path = os.path.join(datadir, datadir_sync)
    datadir_rawsync_path = os.path.join(datadir, datadir_rawsync)

    if not os.path.isdir(datadir_raw_path):
        # Raise an error and exit
        sys.exit("Directory " + datadir_raw_path + " does not exist")
    else:
        print("Found directory " + datadir_raw_path)

    if not os.path.isdir(datadir_sync_path):
        # Raise an error and exit
        sys.exit("Directory " + datadir_sync_path + " does not exist")
    else:
        print("Found directory " + datadir_sync_path)

    # Delete any existing rawsync directory
    if os.path.isdir(datadir_rawsync_path):
        print("Removing existing directory " + datadir_rawsync_path)
        shutil.rmtree(datadir_rawsync_path)
        os.mkdir(datadir_rawsync_path)
    else:
        print("No existing rawsync directory found. Creating a new directory")
        os.mkdir(datadir_rawsync_path)

    # Copy directories that remain unchanged from the sync set
    print("Copying oxts and velodyne_points from sync to rawsync")
    shutil.copytree(os.path.join(datadir_sync_path, 'oxts'), os.path.join(datadir_rawsync_path, 'oxts'))
    shutil.copytree(os.path.join(datadir_sync_path, 'velodyne_points'), os.path.join(datadir_rawsync_path, 'velodyne_points'))

    dirToSync = ("image_00", "image_01", "image_02", "image_03")

    userInput = input("Do you want to continue? [Y/N]: ")
    if userInput.lower() != "y":
        sys.exit("Exiting the program based on user input")

    for directory in dirToSync:
        timestamp_path = os.path.join(directory, 'timestamps.txt')

        # Copy "directory" from raw set to rawsync set for manipulation
        shutil.copytree(os.path.join(datadir_raw_path, directory), os.path.join(datadir_rawsync_path, directory))

        # Replace the timestamp copied from raw set with sync set
        shutil.copy2(os.path.join(datadir_sync_path, timestamp_path), os.path.join(datadir_rawsync_path, timestamp_path))

        # Get list of unsynced files
        timestamp_raw_filepath = os.path.join(datadir_raw_path, timestamp_path)
        timestamp_sync_filepath = os.path.join(datadir_sync_path, timestamp_path)
        removeFiles = locateUnsyncedFiles(timestamp_raw_filepath, timestamp_sync_filepath)
        print("Files to be removed from directory " + directory + " :", removeFiles)

        # Remove the unsynced files and sync directory
#        userInput = input("Do you want to remove the above files? [Y/N]: ")
#        if userInput.lower() != "y":
#            sys.exit("Exiting the program based on user input")
#        else:
        removeUnsyncedFilesAndSync(os.path.join(datadir_rawsync_path, directory), removeFiles)



if __name__ == "__main__":
    main()

