#-*-coding:utf-8-*-
import os
import re
import datetime
today = datetime.date.today().strftime('%Y%m%d')
yesterday = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y%m%d')
#create two files
sc_query_out = open('C:\\Users\\Administrator\\Desktop\\巡检\\%s运行服务.log'%today,'w')
xunjian_out = open('C:\\Users\\Administrator\\Desktop\\巡检\\%s巡检.log'%today,'w')
sc_query = os.popen('sc query').read()
#write datas to fuwu.log
sc_query_out.write('服务 \n'+sc_query)
#run some command
hostname = os.popen('hostname').read()
ipconfig = os.popen('ipconfig /all |findstr IPv4').read()
Guest = os.popen('net user guest|findstr 帐户启用 ').read()
user = os.popen('net user').read()
share = os.popen('net share').read()
ports = os.popen('netstat -ano|findstr 0.0.0.0 ').read()
#write datas to xunjian.log
xunjian_out.writelines('－－－－－－－－－－－－－－－－主机检查开始－－－－－－－－－－－－－－－－ \n'
                  '_______________________________________________________________________________ \n'
                  '主机名 \n%s'
                  '_______________________________________________________________________________ \n'
                  'IP地址和子网掩码 \n%s'
                  '_______________________________________________________________________________ \n'
                  'Guest帐号状态 \n%s'
                  '_______________________________________________________________________________ \n'
                  '用户帐户 \n%s'
                  '_______________________________________________________________________________ \n'
                  '主机开放的共享 \n%s'
                  '_______________________________________________________________________________ \n'
                  '网络开放的端口 \n%s'
                  '_______________________________________________________________________________ \n'
                  '－－－－－－－－－－－－－－－－主机检查结束－－－－－－－－－－－－－－－－ \n'\
%(hostname,ipconfig,Guest,user,share,ports))
#close open files
sc_query_out.close()
xunjian_out.close()
#differents with yunxinfuwu.log
services_differents = open('C:\\Users\\Administrator\\Desktop\\巡检\\%s运行服务比较.log'%today,'w')
try:
    #get differents with today and yesterday
    sc_query_today = open('C:\\Users\\Administrator\\Desktop\\巡检\\%s运行服务.log'%today,'r').read()
    sc_query_yesterday = open('C:\\Users\\Administrator\\Desktop\\巡检\\%s运行服务.log'%yesterday,'r').read()
    services_today = re.findall('SERVICE_NAME: (.*?)\n',sc_query_today)
    services_yesterday = re.findall('SERVICE_NAME: (.*?)\n',sc_query_yesterday)
    services_new = []
    services_old = []
    for service_today in services_today:
        if service_today not in services_yesterday:
            services_new.append(service_today)
    for service_yesterday in services_yesterday:
        if service_yesterday not in services_today:
            services_old.append(service_yesterday)
    #start to write differents
    if services_new !=[]:
        services_differents.write('今天存在而昨天不存在的服务:\n')
        for service_new in services_new:
            services_differents.write('%s\n'%service_new)
    if services_old !=[]:
        services_differents.write('昨天存在而今天不存在的服务:\n')
        for service_old in services_old:
            services_differents.write('%s\n'%service_old)
except:
    services_differents.write('可能是昨天的 %s运行服务.log 不存在'%yesterday)
#close open files
services_differents.close()
#differents with xunjian.log
xunjian_differents = open('C:\\Users\\Administrator\\Desktop\\巡检\\%s巡检比较.log'%today,'w')
try:
    xunjian_today = open('C:\\Users\\Administrator\\Desktop\\巡检\\%s巡检.log'%today,'r').read()
    xunjian_yesterday = open('C:\\Users\\Administrator\\Desktop\\巡检\\%s巡检.log'%yesterday,'r').read()
    xunjians_today = xunjian_today.split('_______________________________________________________________________________ \n')
    xunjians_yesterday = xunjian_yesterday.split('_______________________________________________________________________________ \n')
    if xunjians_today != xunjians_yesterday:
        xunjian_differents.write('巡检.log发生了变化\n')
        for num in range(1,7):
            if xunjians_today[num] !=xunjians_yesterday[num]:
                xunjian_differents.write('--------------------今天的内容--------------------\n'
                                         '%s\n'
                                         '--------------------昨天的内容--------------------\n%s\n'
                                         %(xunjians_today[num],xunjians_yesterday[num]))
except:
    xunjian_differents.write('可能是昨天的 %s巡检.log 不存在'%yesterday)
#close open file
xunjian_differents.close()
