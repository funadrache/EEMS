def DateTimeStr(dt_now, separator):

    DateTimeForm = dt_now.strftime("%Y") + separator \
        + dt_now.strftime("%m") + separator + dt_now.strftime("%d") + separator \
        + dt_now.strftime("%H") + separator + dt_now.strftime("%M") + separator \
        + dt_now.strftime("%S") + separator + dt_now.strftime("%f")
    return DateTimeForm 

import datetime

dt_now = datetime.datetime.now()
print (DateTimeStr(dt_now, "-"))
print (DateTimeStr(dt_now, ","))
