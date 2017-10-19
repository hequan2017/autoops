import datetime

now = datetime.datetime.now()
last_time = now + datetime.timedelta(minutes=-2)

print(last_time)