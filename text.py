from module.func import check_time
import time
a=check_time(time.time())
b=a.check(time.time())
print(b)
time.sleep(1)
b=a.check(time.time())
print(b)
