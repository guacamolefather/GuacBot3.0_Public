import time
def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return "{0} hours, {1} minutes, {2} seconds".format(int(hours),int(mins),sec)
