from tkinter import *
from tkinter import font
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
from io import BytesIO
from googlemaps import Client
from tkinter import messagebox
from spam import spam_max

# Tkinter 초기화
g_Tk = Tk()
g_Tk.geometry("800x600+100+100")
g_Tk.title('주차장 위치 검색 서비스')

# Google Maps API Key
Google_API_Key = 'AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE'  # 여기에 실제 API 키를 입력하세요.
gmaps = Client(key=Google_API_Key)

# 데이터 리스트 초기화
DataList = []
selected_parking_index = None

free_parking_var = BooleanVar()
paid_parking_var = BooleanVar()

# smtp 정보 ++
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"
#주차장 정보 저장
parking_palace_info = str('')
#++ 북마크 정보 저장
Bookmarks = []
#북마크 검색 버튼 토글
showBookmarksFlag = False

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="[경기도 주차장 정보 검색]")
    MainText.pack()
    MainText.place(x=20, y=10)


def InitSearchButton():
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=160, y=90)


def on_click(event):
    global selected_parking_index, parking_palace_info

    # 모든 태그의 배경 색을 기본값으로 되돌림
    for i in range(len(DataList)):
        tag_name = f'tag{i + 1}'
        RenderText.tag_config(tag_name, background='white')

    # 클릭한 위치의 태그 배경 색을 회색으로 변경
    current_index = RenderText.index("@%s,%s" % (event.x, event.y))
    tag_ranges = RenderText.tag_names(current_index)
    for tag in tag_ranges:
        if tag.startswith('tag'):
            RenderText.tag_config(tag, background='gray')
            selected_parking_index = int(tag[3:]) - 1  # 선택한 주차장 인덱스 저장
            parking_palace_info = DataList[selected_parking_index][1]
            update_map(SearchEntry.get())
            break


def SearchButtonAction():
    DataList.clear()
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    city_name = SearchEntry.get()
    # 파일에서 XML 데이터를 읽어옴
    tree = ET.parse('주차장정보현황.xml')
    root = tree.getroot()

    free_parking = free_parking_var.get()
    paid_parking = paid_parking_var.get()
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

        # 주소에서 도시 이름 추출

        if city_name==LOCPLC_LOTNO_ADDR:
            if free_parking and not paid_parking:
                if CHRG_INFO == "무료":
                    DataList.append((PARKPLC_NM, LOCPLC_LOTNO_ADDR, PARKNG_COMPRT_CNT, WKDAY_OPERT_BEGIN_TM,
                                     WKDAY_OPERT_END_TM, CHRG_INFO, CONTCT_NO, SPCLABLT_MATR, SETTLE_METH,
                                     REFINE_WGS84_LAT, REFINE_WGS84_LOGT))
            elif paid_parking and not free_parking:
                if CHRG_INFO != "무료":
                    DataList.append((PARKPLC_NM, LOCPLC_LOTNO_ADDR, PARKNG_COMPRT_CNT, WKDAY_OPERT_BEGIN_TM,
                                     WKDAY_OPERT_END_TM, CHRG_INFO, CONTCT_NO, SPCLABLT_MATR, SETTLE_METH,
                                     REFINE_WGS84_LAT, REFINE_WGS84_LOGT))
            else:
                DataList.append((PARKPLC_NM, LOCPLC_LOTNO_ADDR, PARKNG_COMPRT_CNT, WKDAY_OPERT_BEGIN_TM,
                                 WKDAY_OPERT_END_TM, CHRG_INFO, CONTCT_NO, SPCLABLT_MATR, SETTLE_METH,
                                 REFINE_WGS84_LAT, REFINE_WGS84_LOGT))
        else:
            address_parts = LOCPLC_LOTNO_ADDR.split(' ')
            if len(address_parts) > 1:
                extracted_city = address_parts[1]  # 도시 이름은 주소에서 두 번째 요소로 가정
                # 추출된 도시 이름과 사용자 입력 비교
                if extracted_city == city_name or extracted_city[:2] == city_name[:2]:
                    if free_parking and not paid_parking:
                        if CHRG_INFO == "무료":
                            DataList.append((PARKPLC_NM, LOCPLC_LOTNO_ADDR, PARKNG_COMPRT_CNT, WKDAY_OPERT_BEGIN_TM,
                                             WKDAY_OPERT_END_TM, CHRG_INFO, CONTCT_NO, SPCLABLT_MATR, SETTLE_METH,
                                             REFINE_WGS84_LAT, REFINE_WGS84_LOGT))
                    elif paid_parking and not free_parking:
                        if CHRG_INFO != "무료":
                            DataList.append((PARKPLC_NM, LOCPLC_LOTNO_ADDR, PARKNG_COMPRT_CNT, WKDAY_OPERT_BEGIN_TM,
                                             WKDAY_OPERT_END_TM, CHRG_INFO, CONTCT_NO, SPCLABLT_MATR, SETTLE_METH,
                                             REFINE_WGS84_LAT, REFINE_WGS84_LOGT))
                    else:
                        DataList.append((PARKPLC_NM, LOCPLC_LOTNO_ADDR, PARKNG_COMPRT_CNT, WKDAY_OPERT_BEGIN_TM,
                                         WKDAY_OPERT_END_TM, CHRG_INFO, CONTCT_NO, SPCLABLT_MATR, SETTLE_METH,
                                         REFINE_WGS84_LAT, REFINE_WGS84_LOGT))




    # 필터링된 주차장 정보 표시
    for i in range(len(DataList)):
        tag_name = f'tag{i + 1}'
        RenderText.insert(INSERT, "[", tag_name)
        RenderText.insert(INSERT, i + 1, tag_name)
        RenderText.insert(INSERT, "] ", tag_name)
        RenderText.insert(INSERT, "주차장명: ", tag_name)
        RenderText.insert(INSERT, DataList[i][0], tag_name)
        RenderText.insert(INSERT, "\n", tag_name)
        RenderText.insert(INSERT, "주소: ", tag_name)
        RenderText.insert(INSERT, DataList[i][1], tag_name)
        RenderText.insert(INSERT, "\n", tag_name)
        RenderText.insert(INSERT, "주차구획수: ", tag_name)
        RenderText.insert(INSERT, DataList[i][2], tag_name)
        RenderText.insert(INSERT, "\n", tag_name)
        RenderText.insert(INSERT, "운영시간: ", tag_name)
        RenderText.insert(INSERT, DataList[i][3], tag_name)
        RenderText.insert(INSERT, " - ", tag_name)
        RenderText.insert(INSERT, DataList[i][4], tag_name)
        RenderText.insert(INSERT, "\n", tag_name)
        RenderText.insert(INSERT, "요금정보: ", tag_name)
        RenderText.insert(INSERT, DataList[i][5], tag_name)
        RenderText.insert(INSERT, "\n", tag_name)
        RenderText.insert(INSERT, "전화번호: ", tag_name)
        RenderText.insert(INSERT, DataList[i][6], tag_name)
        RenderText.insert(INSERT, "\n", tag_name)
        RenderText.insert(INSERT, "특이사항: ", tag_name)
        RenderText.insert(INSERT, DataList[i][7], tag_name)
        RenderText.insert(INSERT, "\n", tag_name)
        RenderText.insert(INSERT, "결제방법: ", tag_name)
        RenderText.insert(INSERT, DataList[i][8], tag_name)
        RenderText.insert(INSERT, "\n\n", tag_name)

    RenderText.configure(state='disabled')
    update_map(city_name)

def BookMarkButtonAction():
    global selected_parking_index
    if selected_parking_index is not None:
        selected_parking_info = DataList[selected_parking_index]
        Bookmarks.append(selected_parking_info)


def InitRenderText():
    global RenderText

    text_frame = Frame(g_Tk)
    text_frame.pack()
    text_frame.place(x=10, y=150)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(text_frame, width=30, height=20, borderwidth=2, relief='ridge', font=TempFont)
    RenderText.pack(side=LEFT, fill=BOTH, expand=YES)
    RenderText.bind("<Button-1>", on_click)  # 클릭 이벤트 바인딩

    RenderTextScrollbar = Scrollbar(text_frame, command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=Y)

    RenderText['yscrollcommand'] = RenderTextScrollbar.set


def InitSearchEntry():
    global SearchEntry
    Label(g_Tk, text="<검색할 시 이름>", fg="black", font=("Helvetica", 12)).place(x=10, y=90)
    SearchEntry = Entry(g_Tk, fg="black")
    SearchEntry.place(x=10, y=110)
    free_parking_check = Checkbutton(g_Tk, text="무료", variable=free_parking_var)
    free_parking_check.place(x=10, y=60)

    paid_parking_check = Checkbutton(g_Tk, text="유료", variable=paid_parking_var)
    paid_parking_check.place(x=70, y=60)


def update_map(city_name):
    global DataList
    global Google_API_Key
    global gmaps
    global selected_parking_index

    city_center = gmaps.geocode(f"{city_name} 경기도")[0]['geometry']['location']
    city_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={city_center['lat']},{city_center['lng']}&zoom=13&size=500x500&maptype=roadmap"

    # 선택한 시의 주차장 위치 마커 추가
    for i, info in enumerate(DataList):
        try:
            lat, lng = float(info[-2]), float(info[-1])  # 위도와 경도 추출
            if lat and lng:
                if i == selected_parking_index:
                    city_map_url += f"&markers=color:green%7C{lat},{lng}"
                else:
                    city_map_url += f"&markers=color:red%7C{lat},{lng}"
        except ValueError:
            # "혼합"과 같은 문자열이 포함된 경우, 해당 주차장 정보를 건너뜁니다.
            continue

    city_map_url += f"&key={Google_API_Key}"

    response = requests.get(city_map_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = ImageTk.PhotoImage(img)

    map_label = Label(g_Tk, width=300, height=300, bg='white')
    map_label.pack()
    map_label.place(x=270, y=45)
    map_label.configure(image=img)
    map_label.image = img




def InitRenderGraph():
    # 캔버스 생성
    canvas = Canvas(g_Tk, width=310, height=250, bg='white')
    canvas.place(x=260, y=350)

    # 주차장 정보를 저장할 딕셔너리 초기화
    parking_dic = {city: 0 for city in ['양주', '수원', '안산', '오산', '의왕'
        , '광명', '성남','부천','남양주','시흥','가평']}

    # 파일에서 XML 데이터를 읽어옴
    tree = ET.parse('주차장정보현황.xml')
    root = tree.getroot()

    # 해당 지역의 주차장 정보 가져오기
    for item in root.findall(".//row"):
        LOCPLC_LOTNO_ADDR = item.findtext("LOCPLC_LOTNO_ADDR")
        if LOCPLC_LOTNO_ADDR:
            # 주소에서 도시 이름 추출
            address_parts = LOCPLC_LOTNO_ADDR.split(' ')
            if len(address_parts) > 1:
                extracted_city = address_parts[1]  # 도시 이름은 주소에서 두 번째 요소로 가정
                # 추출된 도시 이름과 사용자 입력 비교
                for city in parking_dic:
                    if extracted_city.startswith(city[:2]):
                        parking_dic[city] += 1

    # 최대 주차장 개수 계산
    #max_count = max(parking_dic.values())
    max_count = spam_max(parking_dic)
    
    # 그래프 영역 크기 계산
    graph_width = 280
    graph_height = 200
    bar_width = graph_width / len(parking_dic)
    bar_gap = 5
    bar_color = 'blue'

    # 막대 그래프 그리기
    for i, (city, count) in enumerate(parking_dic.items()):
        bar_height = (count / max_count) * (graph_height - 20)
        x0 = i * bar_width + bar_gap
        y0 = graph_height
        x1 = (i + 1) * bar_width - bar_gap
        y1 = graph_height - bar_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=bar_color)
        canvas.create_text((x0 + x1) / 2, y1 - 10, text=count, anchor='n')
        canvas.create_text((x0 + x1) / 2, y0 + 10, text=city, anchor='n')

    # 그래프 축과 레이블 그리기
    canvas.create_line(bar_gap, graph_height, graph_width - bar_gap, graph_height)
    canvas.create_line(bar_gap, graph_height, bar_gap, 0)
    canvas.create_text(graph_width / 2, graph_height + 40, text='City', anchor='s')
    canvas.create_text(bar_gap / 2, graph_height / 2, text='Count', anchor='center', angle=90)


def input_mailaddress():
    newWindow = Tk()
    newWindow.title('메일 정보 입력')
    newWindow.geometry("400x300")

    Label(newWindow, text="받는 사람 이메일", font=("Helvetica", 12)).pack(pady=5)
    recipient_entry = Entry(newWindow, fg="black", font=("Helvetica", 12))
    recipient_entry.pack(pady=5)

    def submit_email():
        recipient = recipient_entry.get()
        send_email(recipient)
        newWindow.destroy()

    Button(newWindow, text="전송", command=submit_email, font=("Helvetica", 12)).pack(pady=20)


def send_email(recipient):#++
    global host, port, parking_palace_info, selected_parking_index

    title = str('주차장 위치 정보 메일 전달 시스템')
    senderAddr = str('glanb4277@gmail.com')
    recipientAddr = str(recipient)
    passwd = str('cbbmyxvpefzvgexb')

    selected_parking_info = DataList[selected_parking_index]
    msgtext = (
        f"주차장명: {selected_parking_info[0]}\n"
        f"주소: {selected_parking_info[1]}\n"
        f"주차구획수: {selected_parking_info[2]}\n"
        f"운영시간: {selected_parking_info[3]} - {selected_parking_info[4]}\n"
        f"요금정보: {selected_parking_info[5]}\n"
        f"전화번호: {selected_parking_info[6]}\n"
        f"특이사항: {selected_parking_info[7]}\n"
        f"결제방법: {selected_parking_info[8]}\n"
    )

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Message container를 생성합니다.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    msgPart = MIMEText(msgtext, 'plain')
    msg.attach(msgPart)

    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)  # 로긴을 합니다.
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()

    print("Mail sending complete!!!")

def mail_button():#++
    MailImage = PhotoImage(file="Gmail.png")  # 이미지 파일 경로 설정
    MailButton = Button(g_Tk, image=MailImage, command=input_mailaddress)
    MailButton.image = MailImage  # 이미지 참조 유지
    MailButton.pack()
    MailButton.place(x=125, y=500)

def showBookMark_button():#++
    BookMarkImage = PhotoImage(file="Bookmark.png")  # 이미지 파일 경로 설정
    BookMarkButton = Button(g_Tk, image=BookMarkImage, command=showBookMark)#TODO : 즐겨찾기 액션
    BookMarkButton.image = BookMarkImage  # 이미지 참조 유지
    BookMarkButton.pack()
    BookMarkButton.place(x=25, y=500)

def addBookMark_button():#++
    BookMarkImage = PhotoImage(file="BookmarkPlus.png")  # 이미지 파일 경로 설정
    BookMarkButton = Button(g_Tk, image=BookMarkImage, command=BookMarkButtonAction)  # TODO : 즐겨찾기 액션
    BookMarkButton.image = BookMarkImage  # 이미지 참조 유지
    BookMarkButton.pack()
    BookMarkButton.place(x=235, y=300)

def showBookMark():#++
    global RenderText, showBookmarksFlag
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)

    if showBookmarksFlag:
        # Show search results screen
        showBookmarksFlag = False
        SearchButtonAction()
    else:
        # Show bookmarks screen
        if Bookmarks:
            for i, info in enumerate(Bookmarks):
                tag_name = f'tagBM{i + 1}'
                RenderText.insert(INSERT, "[", tag_name)
                RenderText.insert(INSERT, i + 1, tag_name)
                RenderText.insert(INSERT, "] ", tag_name)
                RenderText.insert(INSERT, "주차장명: ", tag_name)
                RenderText.insert(INSERT, info[0], tag_name)
                RenderText.insert(INSERT, "\n", tag_name)
                RenderText.insert(INSERT, "주소: ", tag_name)
                RenderText.insert(INSERT, info[1], tag_name)
                RenderText.insert(INSERT, "\n", tag_name)
                RenderText.insert(INSERT, "주차구획수: ", tag_name)
                RenderText.insert(INSERT, info[2], tag_name)
                RenderText.insert(INSERT, "\n", tag_name)
                RenderText.insert(INSERT, "운영시간: ", tag_name)
                RenderText.insert(INSERT, info[3], tag_name)
                RenderText.insert(INSERT, " - ", tag_name)
                RenderText.insert(INSERT, info[4], tag_name)
                RenderText.insert(INSERT, "\n", tag_name)
                RenderText.insert(INSERT, "요금정보: ", tag_name)
                RenderText.insert(INSERT, info[5], tag_name)
                RenderText.insert(INSERT, "\n", tag_name)
                RenderText.insert(INSERT, "전화번호: ", tag_name)
                RenderText.insert(INSERT, info[6], tag_name)
                RenderText.insert(INSERT, "\n", tag_name)
                RenderText.insert(INSERT, "특이사항: ", tag_name)
                RenderText.insert(INSERT, info[7], tag_name)
                RenderText.insert(INSERT, "\n", tag_name)
                RenderText.insert(INSERT, "결제방법: ", tag_name)
                RenderText.insert(INSERT, info[8], tag_name)
                RenderText.insert(INSERT, "\n\n", tag_name)
        else:
            RenderText.insert(INSERT, "No bookmarks to display.\n")
        showBookmarksFlag = True

    RenderText.configure(state='disabled')


# 초기화 함수 호출
InitTopText()
InitSearchEntry()
InitSearchButton()
InitRenderText()
update_map('경기')
InitRenderGraph()
#메일 및 즐겨 찾기
mail_button()
showBookMark_button()
addBookMark_button()

g_Tk.mainloop()
