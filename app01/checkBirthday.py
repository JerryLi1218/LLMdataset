import sys
sys.path.append('/home/jerry_li_1218/.local/lib/python3.10/site-packages')
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import xml.etree.ElementTree as ET
import mysql.connector
import sxtwl
import time,datetime


try:
    mydb = mysql.connector.connect(
        host = "192.168.56.101",
        user = "sample-user"   , #user name for mysql
        passwd = "sample-passwd",  #password for mysql
        database = "sampledb"
    )

    mycursor = mydb.cursor()
except :
    print("ERROR")

##lunar birth str##
mycursor.execute("SELECT name, birthday FROM app01_userbirthday WHERE isLunar=2")
lunar_name_birth = mycursor.fetchall()
lunar_name_str = str()
today = datetime.datetime.today()
lunartoday = today - datetime.timedelta(5)

for data in lunar_name_birth:
    if data[-1] == lunartoday and len(lunar_name_birth)==1:
        lunar_name_str = data[0]
    elif data[-1] == lunartoday and len(lunar_name_birth)!=0:
        data = data[0]
        lunar_name_str = data+ " "+ lunar_name_str

if lunar_name_str == '':
    lunar_name_str = '(无人)'
##---------------##


##solar birth str##
mycursor.execute("SELECT name FROM app01_userbirthday WHERE DATEDIFF(birthday, now())=5")
birth_name = mycursor.fetchall()
name_str = str()
if birth_name == [] :
    name_str = '(无人)' 

for name in birth_name:
    if len(birth_name) == 1:
        name = name[0]
        name_str = name
        print("1")
    else:
        name = name[0]
        name_str = name+ " "+ name_str
        print("2")
##---------------##

def mail(name_str):

    my_sender='2406700175@qq.com'    # 发件人邮箱账号
    my_pass = 'ntosyazvoxjndicg'              # 发件人邮箱密码
    my_user='2406700175@qq.com'      # 收件人邮箱账号
    # 2895627740 zyh
    ret=True
    try:
        msg=MIMEText("提醒您,还有5天就是{}的公历生日,是{}的农历生日了".format(name_str, lunar_name_str),'plain','utf-8')
        msg['From']=formataddr(["LJC",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["LJC",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="python大作业测试用例"                # 邮件的主题，也可以说是标题
 
        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    
    except Exception:
        ret=False
    return ret
 


if name_str == '(无人)' and lunar_name_str == '(无人)':
    pass
else:
    ret=mail(name_str)
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")