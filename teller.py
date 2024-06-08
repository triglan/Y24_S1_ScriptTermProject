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

# 텔레그램 봇 토큰
TOKEN = '7247796214:AAG8jaf5pR50vl82zksQQZlEYxVEz48FQ1M'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

def get_parking_data():
    # XML 파일 파싱
    tree = ET.parse('주차장정보현황.xml')
    root = tree.getroot()

    parking_data = []

    # 각 row에서 필요한 데이터 추출
    for item in root.findall(".//row"):
        data = {
            "PARKPLC_NM": item.findtext("PARKPLC_NM"),
            "LOCPLC_LOTNO_ADDR": item.findtext("LOCPLC_LOTNO_ADDR"),
            "PARKNG_COMPRT_CNT": item.findtext("PARKNG_COMPRT_CNT"),
            "WKDAY_OPERT_BEGIN_TM": item.findtext("WKDAY_OPERT_BEGIN_TM"),
            "WKDAY_OPERT_END_TM": item.findtext("WKDAY_OPERT_END_TM"),
            "CHRG_INFO": item.findtext("CHRG_INFO"),
            "CONTCT_NO": item.findtext("CONTCT_NO"),
            "SPCLABLT_MATR": item.findtext("SPCLABLT_MATR"),
            "SETTLE_METH": item.findtext("SETTLE_METH"),
            "REFINE_WGS84_LAT": item.findtext("REFINE_WGS84_LAT"),
            "REFINE_WGS84_LOGT": item.findtext("REFINE_WGS84_LOGT")
        }
        parking_data.append(data)

    return parking_data

def send_message(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc()

def save(user, loc_param):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user TEXT, location TEXT, PRIMARY KEY(user, location))')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES (?, ?)', (user, loc_param))
    except sqlite3.IntegrityError:
        send_message(user, '이미 해당 정보가 저장되어 있습니다.')
        return
    else:
        send_message(user, '저장되었습니다.')
        conn.commit()

def check(user):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user TEXT, location TEXT, PRIMARY KEY(user, location))')
    cursor.execute('SELECT * FROM users WHERE user=?', (user,))
    for data in cursor.fetchall():
        row = f'id: {data[0]}, location: {data[1]}'
        send_message(user, row)

def reply_parking_data(user, location, charge_info=None):
    parking_data = get_parking_data()
    msg = ''
    for park in parking_data:
        if location in park['LOCPLC_LOTNO_ADDR']:
            if charge_info and charge_info not in park['CHRG_INFO']:
                continue
            row = f"{park['PARKPLC_NM']}, {park['LOCPLC_LOTNO_ADDR']}, {park['PARKNG_COMPRT_CNT']} spaces, {park['WKDAY_OPERT_BEGIN_TM']}-{park['WKDAY_OPERT_END_TM']} on weekdays, {park['CHRG_INFO']}, Contact: {park['CONTCT_NO']}\n"
            print(str(datetime.now()).split('.')[0], row)
            if len(row + msg) + 1 > MAX_MSG_LENGTH:
                send_message(user, msg)
                msg = row + '\n'
            else:
                msg += row + '\n'
    if msg:
        send_message(user, msg)
    else:
        send_message(user, f'{location}에 해당하는 주차장 정보가 없습니다.')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        send_message(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('주차장') and len(args) > 1:
        location = args[1]
        charge_info = None
        if len(args) > 2:
            charge_info = args[2]
            if charge_info not in ['유료', '무료']:
                send_message(chat_id, '유료 또는 무료 중 하나를 입력하세요.')
                return
        print(f'주차장 정보 요청: {location}, {charge_info}')
        reply_parking_data(chat_id, location, charge_info)
    # elif text.startswith('저장') and len(args) > 1:
    #     print('try to 저장', args[1])
    #     save(chat_id, args[1])
    # elif text.startswith('확인'):
    #     print('try to 확인')
    #     check(chat_id)
    else:
        send_message(chat_id, """모르는 명령어입니다.\n주차장 [지역명] [유료/무료]\n저장 [지역번호]\n확인 중 하나의 명령을 입력하세요.""")

if __name__ == '__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print('[', today, ']received token:', TOKEN)
    pprint(bot.getMe())

    bot.message_loop(handle)

    print('Listening...')

    while True:
        time.sleep(10)
