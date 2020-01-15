#!/usr/bin/env python3

__author__ = 'ericmhanson'

import time
import os
import logging
import datetime
import argparse
import signal
import sys

if sys.version_info[0] < 3:
    raise RuntimeError('This program requires Python3!')

exit_flag = False
watched_files = {}

logger = logging.getLogger(__file__)


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here
    as well (SIGHUP?) Basically it just sets a global flag, and main() will
    exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    global exit_flag
    # log the associated signal name (the python3 way)
    logger.warning('Received ' + signal.Signals(sig_num).name)
    if sig_num == signal.SIGINT or signal.SIGTERM:
        exit_flag = True


def search_for_magic(filename, start_line, magic_text):
    """
    Read a file, starting from a position line.
    Look for magic text and log a message if found.
    Return the last line number that was read.
    """
    with open(filename) as f:
        line_num = 0
        for line_num, line in enumerate(f, start=1):
            if line_num < start_line:
                continue
            if magic_text in line:
                logger.info('On line {} I found you {}'.format(
                    line_num, magic_text))
        return line_num + 1


def watch_dir(dir_to_watch, fileext, poll_interval, magic_text):
    """watches a directory for magic text"""
    abs_path = os.path.abspath(dir_to_watch)

    for f in os.listdir(abs_path):
        if f.endswith(fileext) and f not in watched_files:
            watched_files[f] = 0
            logger.info('Watching new file: {}'.format(f))

    for f in list(watched_files):
        if f not in os.listdir(abs_path):
            watched_files.pop(f)
            logger.info('Removed file: {}'.format(f))

    for filename in watched_files:
        f = os.path.join(abs_path, filename)
        watched_files[filename] = search_for_magic(
            f, watched_files[filename], magic_text)

    time.sleep(poll_interval)


def create_parser():
    """Creates and returns an argparse cmd line option parser"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i', '--interval', type=float, default=1.0,
                        help='Number of seconds between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')

    return parser


def main():
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s\
                [%(threadName)-12s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)
    app_start_time = datetime.datetime.now()
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '   Running {0}\n'
        '   Started on {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )
    parser = create_parser()
    args = parser.parse_args()

    if not args:
        parser.print_usage()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while not exit_flag:
        try:
            watch_dir(args.path, args.ext, args.interval, args.magic)
        except Exception as e:
            logger.exception('Unhandled error exception: {}'.format(e))

        time.sleep(args.interval)

    uptime = datetime.datetime.now()-app_start_time
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '   Stopped {0}\n'
        '   Uptime was {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, str(uptime))
    )


if __name__ == '__main__':
    main()
