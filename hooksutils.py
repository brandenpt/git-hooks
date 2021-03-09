#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.


import signal
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class TimeoutExpired(Exception):
    pass


def alarm_handler(signum, frame):
    raise TimeoutExpired


def input_with_timeout(input_prompt, input_timeout):
    # set signal handler
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(input_timeout)  # produce SIGALRM in `timeout` seconds

    try:
        return input(input_prompt)
    finally:
        signal.alarm(0)  # cancel alarm
