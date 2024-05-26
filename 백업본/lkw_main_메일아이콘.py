import requests
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser
# 경기도 지하수 관련 데이터 API
url = "https://openapi.gg.go.kr/UndergroundWaterConstruct"
service_key = "261b0fd0fad14a3ba3482ed8cceae48d"

# smtp 정보 ++
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

# 지역코드
SGGUCD = [
    ['41210', '광명시'],
    ['41110', '수원시'],
    ['41310', '성남시'],
    ['41170', '안양시'],
    ['41190', '부천시'],
    ['41220', '평택시'],
    ['41250','동두천시']
]

g_Tk = Tk()
g_Tk.geometry("800x600+100+100")
DataList = []

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
RenderText = None  # 전역 변수로 선언
def SearchButtonAction():
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    city_name = SearchEntry.get()

    sgguCD = get_sgguCD(city_name)
    if sgguCD:
        Search(sgguCD)
    else:
        RenderText.insert(INSERT, "해당 시를 찾을 수 없습니다.")

    RenderText.configure(state='disabled')

def get_sgguCD(city_name):
    for code, name in SGGUCD:
        if name == city_name or name[:2] == city_name[:2]:
            return code
    return None

def Search(sgguCD):
    queryParams = {
        'KEY': service_key,
        'pIndex': '1',  # 페이지 번호
        'pSize': '100',  # 한 페이지당 결과 수
        'SIGUN_CD': sgguCD
    }

    response = requests.get(url, params=queryParams)
    global DataList
    DataList.clear()

    if response.status_code == 200:
        strXml = response.text
        tree = ET.fromstring(strXml)
        for item in tree.iter("row"):
            BIZPLC_NM = item.findtext("BIZPLC_NM")
            LICENSG_DE = item.findtext("LICENSG_DE")
            BSN_STATE_NM = item.findtext("BSN_STATE_NM")
            REFINE_ROADNM_ADDR = item.findtext("REFINE_ROADNM_ADDR")
            REFINE_WGS84_LAT = item.findtext("REFINE_WGS84_LAT")
            REFINE_WGS84_LOGT = item.findtext("REFINE_WGS84_LOGT")
            DataList.append((BIZPLC_NM, LICENSG_DE, BSN_STATE_NM, REFINE_ROADNM_ADDR, REFINE_WGS84_LAT, REFINE_WGS84_LOGT))

        for i in range(len(DataList)):
            RenderText.insert(INSERT, "[")
            RenderText.insert(INSERT, i + 1)
            RenderText.insert(INSERT, "] ")
            RenderText.insert(INSERT, "사업장명: ")
            RenderText.insert(INSERT, DataList[i][0])
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, "허가일자: ")
            RenderText.insert(INSERT, DataList[i][1])
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, "사업상태: ")
            RenderText.insert(INSERT, DataList[i][2])
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, "주소: ")
            RenderText.insert(INSERT, DataList[i][3])
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, "위도: ")
            RenderText.insert(INSERT, DataList[i][4])
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, "경도: ")
            RenderText.insert(INSERT, DataList[i][5])
            RenderText.insert(INSERT, "\n\n")


def InitRenderText():
    global RenderText

    # 텍스트 출력창과 스크롤바를 감싸는 프레임 생성
    text_frame = Frame(g_Tk)
    text_frame.pack()
    text_frame.place(x=10, y=150)  # 프레임 위치 설정

    # 텍스트 출력창 생성
    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(text_frame, width=27, height=20, borderwidth=12, relief='ridge', font=TempFont)
    RenderText.pack(side=LEFT, fill=BOTH, expand=YES)

    # 수직 스크롤바 생성
    RenderTextScrollbar = Scrollbar(text_frame, command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=Y)

    # 스크롤바를 텍스트 위젯과 연결
    RenderText['yscrollcommand'] = RenderTextScrollbar.set



def InitSearchEntry():
    global SearchEntry
    Label(g_Tk, text="<검색할 시 이름>", fg="black", font=("Helvetica", 12)).place(x=10, y=90)
    SearchEntry = Entry(g_Tk, fg="black")
    SearchEntry.place(x=10, y=110)
# def InitRenderGraph():
#     canvas=Canvas(g_Tk,width=280,height=220,bg='blue').place(x=270,y=320)
#     city_names = [city[1] for city in SGGUCD]
#     #parking_lot_counts = [get_parking_lot_count(city_code) for city_code, _ in SGGUCD]
#     parking_lot_counts = {}
#
#     for city_code, city_name in SGGUCD:
#         parking_lot_counts[city_name] = get_parking_lot_count(city_code)
#     print(parking_lot_counts)


def InitRenderGraph():
    # 캔버스 생성
    canvas = Canvas(g_Tk, width=300, height=250, bg='white')
    canvas.place(x=270, y=320)

    # 각 시별 주차장 개수를 가져오기
    city_names = [city[1] for city in SGGUCD]
    parking_lot_counts = [get_parking_lot_count(city_code) for city_code, _ in SGGUCD]

    # 최대 주차장 개수 계산
    max_count = max(parking_lot_counts)

    # 그래프 영역 크기 계산
    graph_width = 280
    graph_height = 200
    bar_width = graph_width / len(city_names)
    bar_gap = 10
    bar_color = 'blue'

    # 막대 그래프 그리기
    for i, count in enumerate(parking_lot_counts):
        bar_height = (count / max_count) * (graph_height-20)
        x0 = i * bar_width + bar_gap
        y0 = graph_height
        x1 = (i + 1) * bar_width - bar_gap
        y1 = graph_height - bar_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=bar_color)
        canvas.create_text((x0 + x1) / 2, y1 -10, text=count, anchor='n')
        canvas.create_text((x0 + x1) / 2,  y0+10, text=city_names[i], anchor='n')

    # 그래프 축과 레이블 그리기
    canvas.create_line(bar_gap, graph_height, graph_width - bar_gap, graph_height)
    canvas.create_line(bar_gap, graph_height, bar_gap, 0)
    canvas.create_text(graph_width / 2, graph_height + 40, text='City', anchor='s')
    canvas.create_text(bar_gap / 2, graph_height / 2, text='Count', anchor='center', angle=90)

def get_parking_lot_count(city_code):
    queryParams = {
        'KEY': service_key,
        'pIndex': '1',
        'pSize': '100',
        'SIGUN_CD': city_code
    }

    response = requests.get(url, params=queryParams)
    if response.status_code == 200:
        tree = ET.fromstring(response.text)
        return sum(1 for _ in tree.iter("row"))
    return 0


def input_mailaddress():
    newWindow = Toplevel(g_Tk)
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


def send_email(recipient):
    global host, port

    title = str('주차장 위치 정보 메일 전달 시스템')
    senderAddr = str('glanb4277@gmail.com')
    recipientAddr = str(recipient)
    passwd = str('cbbmyxvpefzvgexb')
    msgtext = str('n')

    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    # set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    msgPart = MIMEText(msgtext, 'plain')

    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    s = mysmtplib.MySMTP(host, port)

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

def bookMark_button():#++
    BookMarkImage = PhotoImage(file="Bookmark.png")  # 이미지 파일 경로 설정
    BookMarkButton = Button(g_Tk, image=BookMarkImage, command=SearchButtonAction)#TODO : 즐겨찾기 액션
    BookMarkButton.image = BookMarkImage  # 이미지 참조 유지
    BookMarkButton.pack()
    BookMarkButton.place(x=25, y=500)

InitRenderGraph()
InitTopText()
InitSearchEntry()
InitSearchButton()
InitRenderText()
#메일 및 즐겨 찾기
mail_button()
bookMark_button()

g_Tk.mainloop()