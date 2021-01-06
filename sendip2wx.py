# 使用微信接口给微信好友发送消息
import win32serviceutil 
import win32service 
import win32event 
import itchat
import socket
import time
import win32api, win32gui

#获取本机内网IP
def get_local_ip():
    local_ip = ""
    try:
        socket_objs = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
        ip_from_ip_port = [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in socket_objs][0][1]
        ip_from_host_name = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
        local_ip = [l for l in (ip_from_ip_port, ip_from_host_name) if l][0]
    except (Exception) as e:
        print("get_local_ip found exception : %s" % e)
    return local_ip if("" != local_ip and None != local_ip) else socket.gethostbyname(socket.gethostname())

#监控
def monitor_ip():
    #获取内网IP
    nwip = get_local_ip()
    cal = 0
    while True:
        nwip2 = get_local_ip()
        now_localtime = time.strftime("%H:%M:%S", time.localtime())
        str_now_localtime = now_localtime + "\n"
        #内网ip有变化了或者第一次运行脚本(电脑重启时),发送内网ip给微信
        if nwip2 != nwip or cal==0:
            nwip = nwip2
            #限制发送微信信息的时间段
            if "07:30:00" < now_localtime < "23:59:59":
                #自动登录方法，hotReload=True可以缓存，不用每次都登录,但是第一次执行时会出现一个二维码，需要手机微信扫码登录
                itchat.auto_login(hotReload=True)
                #调用微信接口发送消息给文件传输助手
                itchat.send(nwip2, 'filehelper')
                itchat.logout()
        #每24小时更新cal为0
        if cal != 0 and cal % 86400 == 0:
            cal = 0
        #每隔60s写一次日志
        with open ('sendip2wx.log' ,'a',encoding='utf-8') as f:
          f.write(str_now_localtime)
        time.sleep(60)
        cal += 60

def main():
    '''
    #程序入口#
    '''
    #关闭cmd窗口
    ct = win32api.GetConsoleTitle()
    hd = win32gui.FindWindow(0,ct)
    win32gui.ShowWindow(hd,0)
    #监控ip
    monitor_ip()


if __name__ == '__main__': 
    '''
    #运行#
    '''   
    main()