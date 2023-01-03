# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 22:56:01 2023

Requirement: yfinance

@author: NtRdeMtrX
"""
import os
import datetime
import time as T_module

import yfinance as yf
import requests
import urllib
import zipfile
import shutil

def future_daily_download(daily_number = 1):
    DL_directory = './Future_Daily_Download/'
    # 檢查目錄是否存在 
    if os.path.isdir(DL_directory):
        print("The directory is already exist.")
    else:
        print(f"The directory is not exist. Create directory \"{DL_directory}\"")
        os.makedirs(DL_directory)
    
    data_df = yf.Ticker('^TWII').history(period = str(daily_number) + 'd')
    DT_series = data_df.index
    
    for DT in DT_series:
        DT_str = datetime.datetime.strftime(DT, "%Y_%m_%d")       

        DL_filename = 'Daily_' + DT_str + '.zip' 
        print(f"Downloading {DL_filename} ....")
        DL_url = 'https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/' + DL_filename
        if requests.get(DL_url, verify=False).status_code >= 400:
            print(requests.get(DL_url, verify=False))
        else:
            urllib.request.urlretrieve(DL_url, DL_directory + DL_filename)
            zipped_file = DL_directory + DL_filename
            print(f"Unzipping {DL_filename} ....")
            with zipfile.ZipFile(zipped_file,"r") as zip_ref:
                zip_ref.extractall(DL_directory)

            os.remove(zipped_file)
            
            unzipped_filename = DL_filename.replace('.zip', '.csv')
            mv_path = './' # 解壓後欲存放之資料夾路徑
            shutil.move(DL_directory + unzipped_filename, mv_path + unzipped_filename)

def main():
    while True: 
        Tx = datetime.datetime.now()
        if Tx.hour == 8 and Tx.minute == 30:
        ###### Future Daily Download ######    
            future_daily_download()
        
        ###### Awaken time setting ######
        if Tx.time() <= datetime.time(8,30,0):
            wake_time = datetime.datetime(Tx.year, Tx.month, Tx.day, 8, 25, 0)    
        else:
            Tx_next = Tx + datetime.timedelta(days=+1)
            wake_time = datetime.datetime(Tx_next.year, Tx_next.month, Tx_next.day, 8, 25, 0)
        #sleep_time = int(wake_time.timestamp() - Tx.timestamp())
        sleep_time = (wake_time - Tx).seconds
        sleep_time_hr = int(sleep_time/3600)
        sleep_time_min = int((sleep_time % 3600) /60)
        sleep_time_sec = sleep_time % 60
        print("\n{:^111}\n".format("ZZZZzzzzzz  System Sleep Time  {:02d}:{:02d}:{:02d}  zzzzzzZZZZ")\
                                    .format(sleep_time_hr, sleep_time_min, sleep_time_sec))
        
        T_module.sleep(sleep_time)  # Sleep in Second Unit
        sleep_time = 0.001
        
if __name__ == "__main__":
    future_daily_download()
    main()