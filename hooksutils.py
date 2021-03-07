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
