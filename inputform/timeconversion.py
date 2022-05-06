##############for time conversion

#do not modify this code it may effect the time in webpage
def timeconvert(presenthour):
    if presenthour==24:
        timeconvert.presenthour=0
    if presenthour>=12:
        if presenthour==12:
            timeconvert.this_hour=12
            timeconvert.am_or_pm='PM'
        elif presenthour>12:
            timeconvert.this_hour=presenthour-12
            timeconvert.am_or_pm='PM'
    else:
        timeconvert.this_hour= presenthour
        timeconvert.am_or_pm='AM'


def nexthourconvert(nexthour):
    if nexthour==24:
        nexthourconvert.next_hour=12
        nexthourconvert.next_hour_am_or_pm='AM'
    elif nexthour>=12:
        if nexthour==12:
            nexthourconvert.next_hour=12
            nexthourconvert.next_hour_am_or_pm='PM'
        elif nexthour>12:
            nexthourconvert.next_hour=nexthour-12
            nexthourconvert.next_hour_am_or_pm='PM'
    else:
        nexthourconvert.next_hour= nexthour
        nexthourconvert.next_hour_am_or_pm='AM'