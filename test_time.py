import time

currenttime = time.asctime(time.localtime(time.time()))
current_token = currenttime.split()
print(current_token[:3])
