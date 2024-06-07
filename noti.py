#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from datetime import date, datetime
import traceback
import xml.etree.ElementTree as ET

TOKEN = '7247796214:AAG8jaf5pR50vl82zksQQZlEYxVEz48FQ1M'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

def getDataFromXML():
    res_list = []

    # 파일에서 XML 데이터를 읽어옴
    tree = ET.parse('주차장정보현황.xml')
    root = tree.getroot()

    # 해당 지역의 주차장 정보 가져오기
    for item in root.findall(".//row"):
        PARKPLC_NM = item.findtext("PARKPLC_NM")
        LOCPLC_LOTNO_ADDR = item.findtext("LOCPLC_LOTNO_ADDR")
        PARKNG_COMPRT_CNT = item.findtext("PARKNG_COMPRT_CNT")
        WKDAY_OPERT_BEGIN_TM = item.findtext("WKDAY_OPERT_BEGIN_TM")
        WKDAY_OPERT_END_TM = item.findtext("WKDAY_OPERT_END_TM")
        CHRG_INFO = item.findtext("CHRG_INFO")
        CONTCT_NO = item.findtext("CONTCT_NO")
        SPCLABLT_MATR = item.findtext("SPCLABLT_MATR")
        SETTLE_METH = item.findtext("SETTLE_METH")
        REFINE_WGS84_LAT = item.findtext("REFINE_WGS84_LAT")
        REFINE_WGS84_LOGT = item.findtext("REFINE_WGS84_LOGT")

        row = f'{PARKPLC_NM}, {LOCPLC_LOTNO_ADDR}, {PARKNG_COMPRT_CNT}, {WKDAY_OPERT_BEGIN_TM}-{WKDAY_OPERT_END_TM}, {CHRG_INFO}, {CONTCT_NO}, {SPCLABLT_MATR}, {SETTLE_METH}, {REFINE_WGS84_LAT}, {REFINE_WGS84_LOGT}'
        if row:
            res_list.append(row.strip())

    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run():
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user = data[0]
        print(user)
        res_list = getDataFromXML()
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES (?, ?)', (user, r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print(str(datetime.now()).split('.')[0], r)
                if len(r + msg) + 1 > MAX_MSG_LENGTH:
                    sendMessage(user, msg)
                    msg = r + '\n'
                else:
                    msg += r + '\n'
        if msg:
            sendMessage(user, msg)
    conn.commit()

if __name__ == '__main__':
    today = date.today()
    print('[', today, ']received token :', TOKEN)

    pprint(bot.getMe())

    run()
