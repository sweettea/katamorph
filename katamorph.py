# Copyright the katamorph authors.

import argparse, sys, os, shutil

try:
    import dmpy as dm
except ImportError:
    raise ImportError("dmpy module not found -- please install from "
                      + "https://github.com/bmr-cymru/dmpy")

from lib import *

def exception_swallower(exception_type, exception, traceback):
    print(f"{exception_type.__name__}: {exception}")

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="""
        The path to the device which is full (e.g.
        /dev/mapper/my_full_device)""")
    #parser.add_argument("-v", "--verbose", help="""
    #    Emit debugging information (commands and ioctls at level 1, output
    #    thereof at level 2""" ,
    #    action="count");
    parser.add_argument("--debug", help="Print debugging info", action="store_true")
    parser.add_argument("--tmpfilesz", help="""
        Temp file size. Two tempfiles are needed, each of this size. This
        option overrides the environment variable TMPFILESZ, if it is set.
        Defaults to a tenth of the full device's presented size""")
    parser.add_argument("--loopbackdir", help="""
        Directory to store temporary files in. This option overrides the
        environment variable LOOPBACK_DIR, if it is set. Must have enough
        free space for two files of size <tmpfilesz>.""")
    parser.add_argument("--", help="Print debugging info", action="store_true")
    args = parser.parse_args()

    if not args.debug:
        sys.excepthook = exception_swallower

    try:
        dm.driver_version()
    except PermissionError as e:
        raise PermissionError("""Cannot communicate with device-mapper.
Try rerunning as root""") from e

    full_device = DmDevice(path = args.path)
    
    args.tmpfilesz = args.tmpfilesz or os.environ["TMPFILESZ"]
    args.tmpfilesz = int (args.tmpfilesz
                          or full_device.get_size() / device.SECTOR_SIZE)
    args.loopbackdir = args.loopbackdir or os.environ["LOOPBACK_DIR"]
    args.loopbackdir = args.loopbackdir or "/tmp"

    # Check that loopbackdir has enough space for two tmpfilesz files.
    (total, used, free) = shutil.disk_usage(args.loopbackdir)
    if free < 2 * args.tmpfilesz:
        raise IOError(f"Insufficient space available in {args.loopbackdir}"
                      + f" for two files of size {args.tmpfilesz} bytes."
                      + " Try adjusting one or both parameters")

    # Set up tmp devices.

    mktemp


    

    # TBD
