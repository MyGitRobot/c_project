# -*- coding: utf-8 -*-
"""Explanation Codes of c_p"""
'''Notes: some codes have been replaced with '***' for certain reason'''

import os
import requests
import re
import subprocess
import m3u8
import time


def ppp():
    try:
        base_url = input('Input the video link:')  # get target url
        html = requests.get(base_url, timeout=15).text  # get text of html
        script = re.findall(r'(***)', html)[0]  # get text of a <script></script>
        script = script.replace('\/', '/')  # tidy the text
        head = re.findall(r'(***)', script)[0]  # get head url
        master_url = re.findall(r'(***)', script)[0]  # get m3u8 master url
        
        hd_select = re.findall('(***)', script)[0]  # get all optional resolution
        hd_select = hd_select.split(',')  # tidy
        hd = input(f'Choose the resolution{hd_select}:')  # get target resolution
        
        while True:
            if hd in hd_select:  # ensure correct resolution
                hd_index = hd_select.index(hd)
                break
            else:
                hd = input(f'Choose the correct resolution{hd_select}:')
        
        m3u8_master = m3u8.loads(requests.get(master_url).text)  # load m3u8 master
        m3u8_url = m3u8_master.data['playlists'][hd_index]['uri']  # get m3u8 url
        m3u8_url = head + m3u8_url  # form true m3u8 url
        file_name = re.findall(r'(***)', m3u8_url)[0]  # set filename
        m3u8_res = requests.get(m3u8_url)  # get content of m3u8
        ts_url = m3u8.loads(m3u8_res.text)  # load m3u8
        
        with open(f'{file_name}.ts', 'wb') as f:
            count = 0
            for seg in ts_url.data['segments']:
                url = head + seg['uri']  # form true ts url
                print('\r' + f'Downloading...{round(100 * count / len(ts_url.data["segments"]))}%', end='', flush=True)  # display progress bar
                count += 1
                r = requests.get(url, timeout=60)  # get ts file
                f.write(r.content)
            print('\r' + f'Downloaded，Saving...')
        
        subprocess.run(['ffmpeg', '-i', f'{file_name}.ts', f'{file_name}.mp4'])  # convert ts to mp4, require ffmpeg
        os.remove(f'{file_name}.ts')  # delete ts
        print(f'{file_name}.mp4 saved.')
        time.sleep(3)
    
    except (TimeoutError, requests.exceptions.Timeout):
        print('Poor network, check it out...')
        time.sleep(3)
        
    except Exception as e:
        print(f'Error...{e}')
        time.sleep(3)


if __name__ == '__main__':
    # check if program is modified
    ppp()
    # if modified, program won't work normally
