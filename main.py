from datetime import datetime

now_time = datetime.now()
utc_time = datetime.utcnow()

print(now_time)#当前时间，电脑显示的时间
print(utc_time)#utc时间，伦敦时间

with open('clash.yml','w+') as f:
    f.writelines('{}'.format(now_time))
print('1')
