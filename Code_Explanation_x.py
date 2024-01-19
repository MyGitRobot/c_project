'''explanation of c_x'''

'''Note: Some codes have been replaced with '***' for certain reason'''

import os
import time
import requests
import re
import subprocess


def main():
    base_url = input('Input the video link:')  # get link of video
    
    try:
        html = requests.get(base_url, timeout=10).text  # get text of html
        hls = re.findall(r'(***)', html)[0]  # get text included link of m3u8 file
        src = requests.get(hls).text  # get text of m3u8 file
        hd_select = re.findall(r'(***)', src)  # get all resolution
        m3u8_select = re.findall(r'(***)', src)  # get m3u8 url
        hd = input(f'Choose the video resolution{hd_select}:')  # get choice of resolution
        
        while True:
            if hd in hd_select:  # ensure input resolution is correct
                index = hd_select.index(hd)
                break
            else:
                hd = input(f'Choose the correct resolution{hd_select}:')
        
        m_code = m3u8_select[index]  # get m3u8 url of given resolution
        file_name = re.findall(r'(***)', m_code)[0]  # set the output filename
        head_url = re.findall(r'(***)', hls)[0]  # get head url (https://...)
        m3u8_url = head_url + f'{m_code}'  # form correct m3u8 url
        res = requests.get(m3u8_url)  # get content of m3u8 file
        m3u8 = re.findall(r'(***)', res.text)  # get ts name
        
        with open(f'{file_name}.ts', 'wb') as f:
            for i in range(0, len(m3u8)):
                prog = round(i / len(m3u8) * 100)
                print('\r' + f'Downloading...{prog}%', end='', flush=True)  # display progress bar
                ts_url = head_url + m3u8[i]  # form correct ts url
                ts = requests.get(ts_url)  # get ts file
                f.write(ts.content)  # save ts file
        print('\r' + 'Finished. Saving...')
        subprocess.run(['ffmpeg', '-i', f'{file_name}.ts', f'{file_name}.mp4'])  # convert ts to mp4, require ffmpeg
        os.remove(f'{file_name}.ts')  # delete ts file
        print(f'{file_name}.mp4 saved.')
        time.sleep(3)
    
    except (TimeoutError, requests.exceptions.Timeout):
        print('Poor network, check it out...')
        time.sleep(3)
    
    except Exception as e:
        print(f'Error...{e}')
        time.sleep(3)


if __name__ == '__main__':
    # if file is not modified, main() will be executed
    main()
    # else, report error
