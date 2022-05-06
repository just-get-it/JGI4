



from userdetail.models import detail,staff_Categories,seller_Categories,list_of_holidays

import datetime



def getPlannedDate(details,start_date,lap):
    increased_by1=start_date
    while lap>0:
        # print("here")
        increased_by1=increased_by1+datetime.timedelta(days=1)
        holiday_or_not=False
        weeks_incres=increased_by1.weekday()
        if details.staff:
            holiday_by_staff=details.staff_category.holidays.all()
        else:
            holiday_by_staff=details.seller_category.holidays.all()
        for ij in holiday_by_staff:
            if ij.num == weeks_incres:
                holiday_or_not=True
        if holiday_or_not:
            pass
        else:
            objs=list_of_holidays.objects.filter(date_of_holiday=increased_by1,users=details)
            if objs.count()>0:
                holiday_or_not=True
        while holiday_or_not:
            increased_by1=increased_by1+datetime.timedelta(days=1)
            holiday_or_not=False
            weeks_incres=increased_by1.weekday()
            if details.staff:
                holiday_by_staff=details.staff_category.holidays.all()
            else:
                holiday_by_staff=details.seller_category.holidays.all()
            # print("By Week ",holiday_or_not)
            for ij in holiday_by_staff:
                if ij.num == weeks_incres:
                    holiday_or_not=True
            if holiday_or_not:
                pass
            else:
                objs=list_of_holidays.objects.filter(date_of_holiday=increased_by1,users=details)
                # print(objs.first())
                if objs.count()>0:
                    holiday_or_not=True
            # print("Here")
        lap-=1
    return increased_by1
