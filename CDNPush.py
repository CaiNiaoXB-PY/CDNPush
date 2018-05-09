# -*- coding:utf-8 -*-
#coding by kayserzhang
#环境要求：Python 2.7 selenium 2.53.1 firefox 46.0
#import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import cookielib
import urllib
import re
import sys
import urllib2
from binascii import b2a_hex,a2b_hex
from Crypto.Cipher import DES
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import datetime
import pytesseract
#创建一个浏览器对象
driver = webdriver.Firefox()
url='https://si.chinanetcenter.com/'
#调用URL参数打开网页
driver.get(url)
#等待0.5秒，让页面完全加载
sleep(0.5)
#对登陆页面截图并保存
driver.get_screenshot_as_file('C:\CDNPush\yzm.png')
#定位到验证码位置并获取到坐标值
element=driver.find_element_by_id("jcaptchaImage")
left=int(element.location['x'])+10
top=int(element.location['y'])+8
#推算出验证码宽度及高度
right=left+65
bottom=top+30
#读取登陆页面截图
im=Image.open('C:\CDNPush\yzm.png')
#根据获取到的验证码坐标值截取验证码并保存
im=im.crop((left,top,right,bottom))
im.save('C:\CDNPush\yzmnew.png')
#读取保存的验证码图片
im = Image.open('C:\CDNPush\yzmnew.png')
#识别并读取验证码图片的字符串
vcode = pytesseract.image_to_string(im)
#去除读取的验证码字符串中的空格
vcode = vcode.replace(" ","")
#在登陆页面填入登陆信息并点击登陆
driver.find_element_by_name("username").send_keys("登陆用户名")
driver.find_element_by_name("password").send_keys("登陆密码")
driver.find_element_by_name("jcaptcha").send_keys(vcode)
driver.find_element_by_id("login-btn").click()
#由于验证码识别存在识别错误的情况，所以多循环几次，以保证登陆成功
for i in range(20):
    
	driver.find_element_by_name("username").clear()
	driver.find_element_by_name("password").clear()
	driver.find_element_by_name("jcaptcha").clear()
	driver.find_element_by_id("jcaptchaImage").click()
	sleep(2)
	driver.get_screenshot_as_file('C:\CDNPush\yzm.png')
	element=driver.find_element_by_id("jcaptchaImage")
	left=int(element.location['x'])
	top=int(element.location['y'])
	right=left+90
	bottom=top+38
	im=Image.open('C:\CDNPush\yzm.png')
	im=im.crop((left,top,right,bottom))
	im.save('C:\CDNPush\yzmnew.png')
	im = Image.open('C:\CDNPush\yzmnew.png')
	vcode = pytesseract.image_to_string(im)
	vcode = vcode.replace(" ","")
	#输入用户名
	driver.find_element_by_name("username").send_keys("登陆用户名")
	#输入密码
	driver.find_element_by_name("password").send_keys("登陆密码")
	#输入验证码
	driver.find_element_by_name("jcaptcha").send_keys(vcode)
	#点击登录
	driver.find_element_by_id("login-btn").click()
    #获取当前页面URL
	url = driver.current_url
	#若当前页面的URL与登陆后的URL一致，则表示已登陆成功，跳出循环，否则继续
	if url == "https://si.chinanetcenter.com/purview/welcome.html" :
		break
	else :
		pass
sleep(2)
#在登陆后页面找到“内容管理”链接并点击
driver.find_element_by_xpath("//div[@id='j-producet-list']/ul[@id='j-commonFuncLists']/li[1]/a").click()
sleep(2)
#在页面找到“目录刷新”并点击
driver.find_element_by_xpath("//div[@id='J_MainLeftNav']/ul[1]/li[1]/ul[1]/li[2]/a").click()
sleep(2)
#定义需要提交的url
urldata = "url1" + '\n' + "url2" + '\n' + "url3" + '\n' + "url4"
#定位到多行文本框并传入需提交的URL地址
driver.find_element_by_id("J_dir_text").send_keys(urldata)
sleep(2)
#截图保存，便于审计
driver.get_screenshot_as_file('C:\\CDNPush\\Push_1.png')
#定位到提交按钮并点击
driver.find_element_by_xpath("//div[@class='formsubmit']/a[@id='J_submit_Btn']/span").click()
#截图保存，便于审计
driver.get_screenshot_as_file('C:\\CDNPush\\Push_2.png')
sleep(2)
#关闭浏览器
driver.close()
#退出浏览器对象
driver.quit()
#引入邮件系统依赖的包
import codecs
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib
import time
#定义邮件函数并创建邮件对象将cdn推送结果发送指定邮箱
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))
from_addr ='发件邮箱'
password = '发件邮箱密码'
to_addr = '收件邮箱'
cc_addr = '抄送邮箱'
smtp_server = '发件服务器'
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Cc'] = cc_addr
msg['Subject'] = Header(u'CDN成功完成推送通知', 'utf-8').encode()
# 添加邮件内容
msg.attach(MIMEText( u'已成功完成CDN推送！', 'plain', 'utf-8'))
# 添加附件
with open("C:\\CDNPush\\Push_1.png", 'rb') as f:
     mime = MIMEBase('Image', 'png', filename="Push_1.png")
     mime.add_header('Content-Disposition', 'attachment', filename="Push_1.png")
     mime.add_header('Content-ID', '<0>')
     mime.add_header('X-Attachment-Id', '0')
     mime.set_payload(f.read())
     encoders.encode_base64(mime)
     msg.attach(mime)
with open("C:\\CDNPush\\Push_2.png", 'rb') as g:
     mime = MIMEBase('Image', 'png', filename="Push_2.png")
     mime.add_header('Content-Disposition', 'attachment', filename="Push_2.png")
     mime.add_header('Content-ID', '<0>')
     mime.add_header('X-Attachment-Id', '0')
     mime.set_payload(g.read())
     encoders.encode_base64(mime)
     msg.attach(mime)     
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr,[to_addr]+[cc_addr], msg.as_string())
server.quit()
