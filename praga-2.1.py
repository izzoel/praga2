import sys
import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
import time as t
# from RPLCD.i2c import CharLCD
from datetime import datetime, date, time
from test import test
from openpyxl import load_workbook, workbook
# from antispoofing.test import test

a = (0b00000, 0b00000, 0b00001, 0b00011, 0b00111, 0b00110, 0b01100, 0b01100)
b = (0b00000, 0b11111, 0b11111, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000)
c = (0b00000, 0b00000, 0b10000, 0b11000, 0b11100, 0b01100, 0b00110, 0b00110)
d = (0b01100, 0b01100, 0b00110, 0b00111, 0b00011, 0b00001, 0b00000, 0b00000)
e = (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b11111, 0b00000)
f = (0b00110, 0b00110, 0b01100, 0b11100, 0b11000, 0b10000, 0b00000, 0b00000)

# lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
#               cols=20, rows=4, dotsize=8,
#               charmap='A02',
#               auto_linebreaks=True,
#               backlight_enabled=True)
#
# lcd.create_char(0, a)
# lcd.create_char(1, b)
# lcd.create_char(2, c)
# lcd.create_char(3, d)
# lcd.create_char(4, e)
# lcd.create_char(5, f)
#
#

path = 'img'
images = []
nama = []
# jabatan = []
myList = os.listdir(path)
listnama = []



check = datetime.now().strftime('%H:%M:%S')

absenMasuk = time.strftime(time(7, 59, 59), '%H:%M:%S')
absenMasukClosed = time.strftime(time(12, 59, 59), '%H:%M:%S')
absenPulang = time.strftime(time(21, 0, 0), '%H:%M:%S')
absenPulangClosed = time.strftime(time(23, 59, 59), '%H:%M:%S')

# elif check >= '21:00:00':
#     denda = (1800000 * 0.5) / 100;

for namaImg in myList:
    curImg = cv2.imread(f'{path}/{namaImg}')
    images.append(curImg)
    nama.append(os.path.splitext(namaImg)[0])
    # jabatan.append(os.path.splitext(namaImg)[0].split('-')[1])




# def lcdLoading():
#     lcd.write_string('\x00')
#     t.sleep(.1)
#     lcd.write_string('\x01')
#     t.sleep(.1)
#     lcd.write_string('\x02')
#     t.sleep(.1)
#     lcd.cursor_pos = (1, 2)
#     lcd.write_string('\x05')
#     t.sleep(.1)
#     lcd.cursor_pos = (1, 1)
#     lcd.write_string('\x04')
#     t.sleep(.1)
#     lcd.cursor_pos = (1, 0)
#     lcd.write_string('\x03')
#
#     lcd.cursor_pos = (0, 4)
#     lcd.write_string('MEMULAI')
#     t.sleep(.1)
#     lcd.cursor_pos = (1, 4)
#     lcd.write_string('SISTEM')
#     t.sleep(.2)
#     lcd.write_string('.')
#     t.sleep(.2)
#     lcd.write_string('.')
#     t.sleep(.2)
#     lcd.write_string('.')
#     t.sleep(.4)
#     lcd.clear()

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def pulang(nameDetect, check):
    file = pd.read_excel('al.xlsx')
    tanggal = str(datetime.now().date())
    pulang = check
    nama = nameDetect

    label = test(image=frame,
                 model_dir='antispoofing/resources/anti_spoof_models/',
                 device_id=0)

    if label == 1:
        if nama not in listnama:

            jabatan = nama.split('-')[1]

            if jabatan == 'SEKRETARIS DESA':
                gaji = 1800000
            elif jabatan == 'KAUR KEUANGAN':
                gaji = 1700000
            elif jabatan == 'KAUR UMUM' or jabatan == 'KASI':
                gaji = 1250000
            elif jabatan == 'KADUS':
                gaji = 1100000

            if (check >= '21:00:00') & (check <= '22:00:59'):
                denda = 0;
            elif (check >= '22:01:00') & (check <= '22:30:59'):
                denda = gaji*0.5/100
            elif (check >= '22:31:00') & (check <= '23:00:59'):
                denda = gaji*1/100
            elif (check >= '23:01:00') & (check <= '23:30:59'):
                denda = gaji*1.5/100
            elif (check >= '23:31:00') & (check <= absenPulangClosed):
                denda = gaji*1.5/100


            file.loc[(file.Nama == nama.split('-')[0]) & (
                file.Tanggal == tanggal) & (file.Datang.notnull()) & (file.Pulang.isnull()), 'Pulang'] = pulang
            # print(file.loc[(file.Nama == nama.split('-')[0])])
            listnama.append(nama)

            file.to_excel('al.xlsx',  index=False)

        cv2.rectangle(img, (150, 50), (510, 100), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, 'ABSEN PULANG', (200, 85),cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
    #     print('asli')
    # else:
    #     print('foto')

def datang(nameDetect, check, frame):
    file = pd.read_excel('al.xlsx')
    tanggal = str(datetime.now().date())
    datang = check
    pulang = None
    nama = nameDetect

    label = test(image=frame,
                 model_dir='antispoofing/resources/anti_spoof_models/',
                 device_id=0)

    if label == 1:
        if nama not in listnama:
            listnama.append(nameDetect)
            jabatan = nama.split('-')[1]

            if jabatan == 'SEKRETARIS DESA':
                gaji = 1800000
            elif jabatan == 'KAUR KEUANGAN':
                gaji = 1700000
            elif jabatan == 'KAUR UMUM' or jabatan == 'KASI':
                gaji = 1250000
            elif jabatan == 'KADUS':
                gaji = 1100000

            if (check >= '21:00:00') & (check <= '22:00:59'):
                denda = 0
            elif (check >= '22:01:00') & (check <= '22:30:59'):
                denda = gaji*0.5/100
            elif (check >= '22:31:00') & (check <= '23:00:59'):
                denda = gaji*1/100
            elif (check >= '23:01:00') & (check <= '23:30:59'):
                denda = gaji*1.5/100
            elif (check >= '23:31:00') & (check <= absenMasukClosed):
                denda = gaji*1.5/100


            df2 = pd.DataFrame([[nama.split('-')[0],jabatan, tanggal, datang, pulang, denda]],
                               columns=['Nama','Jabatan', 'Tanggal', 'Datang', 'Pulang','Denda'])

            res = pd.concat([file, df2], ignore_index=True)


            # if (check >= '21:00:00') & (check <= '22:00:00'):
            #     denda = 0;
            #
            # elif (check >= '22:00:01') & (check <= '23:00:00'):
            #     denda = 100;


            # tl.loc[(tl['CHECKTIME'] >= hari + ' 00:00:00') & (tl['CHECKTIME'] <= hari + ' 06:59:59'), ['KET', 'DENDA']] = ['CLOSED', 0]

            # res.loc[res['Datang'] >= '07:00:00']

            # print(res.loc[res['Datang'] >= '07:00:00'])

            print(df2)
            res.to_excel('al.xlsx',  index=False)

        cv2.rectangle(img, (150, 50), (510, 100), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, 'ABSEN DATANG', (200, 85),
                    cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
    #     print('asli')
    #
    # else:
    #     print('foto')

encodeListKnown = findEncodings(images)


# print("Loading:")
# # animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
# animation = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
# for i in range(len(animation)):
#     t.sleep(0.2)
#     sys.stdout.write("\r" + animation[i % len(animation)])
#     sys.stdout.flush()
# print("\n")
#
# print("Status:")
# # lcdLoading()
# print("[Encoding Selesai]")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)




while True:
    # lcd.clear()
    success, img = cap.read()
    frame = img
    frameRe = cv2.resize(img, (800, 600))
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgSmall)
    encodeCurFrame = face_recognition.face_encodings(imgSmall, faceCurFrame)

    w, h, c = img.shape
    new_w = int(w * 1.5)
    new_h = int(h * 1.5)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            nameDetect = nama[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, nameDetect, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)

            if absenMasuk <= check <= absenMasukClosed:
                datang(nameDetect, check, frame)

            elif check >= absenPulang:
                pulang(nameDetect, check)

    cv2.imshow('webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

