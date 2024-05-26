from tkinter import *
from tkinter import font
import xml.etree.ElementTree as ET

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

RenderText = None

def SearchButtonAction():
    DataList.clear()
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    city_name = SearchEntry.get()
    print(city_name)
    # 파일에서 XML 데이터를 읽어옴
    tree = ET.parse('api.xml')
    root = tree.getroot()

    # 해당 지역의 주차장 정보 가져오기
    for item in root.findall(".//row"):
        PARKPLC_NM = item.findtext("PARKPLC_NM")
        LOCPLC_ROADNM_ADDR = item.findtext("LOCPLC_ROADNM_ADDR")
        PARKNG_COMPRT_CNT = item.findtext("PARKNG_COMPRT_CNT")
        WKDAY_OPERT_BEGIN_TM = item.findtext("WKDAY_OPERT_BEGIN_TM")
        WKDAY_OPERT_END_TM = item.findtext("WKDAY_OPERT_END_TM")
        CHRG_INFO = item.findtext("CHRG_INFO")
        CONTCT_NO = item.findtext("CONTCT_NO")
        SPCLABLT_MATR = item.findtext("SPCLABLT_MATR")
        SETTLE_METH = item.findtext("SETTLE_METH")

        # 주소에서 도시 이름 추출
        address_parts = LOCPLC_ROADNM_ADDR.split(' ')
        if len(address_parts) > 1:
            extracted_city = address_parts[1]  # 도시 이름은 주소에서 두 번째 요소로 가정합니다
            # 추출된 도시 이름과 사용자 입력 비교
            if extracted_city == city_name or extracted_city[:2] == city_name[:2]:
                DataList.append((PARKPLC_NM, LOCPLC_ROADNM_ADDR, PARKNG_COMPRT_CNT, WKDAY_OPERT_BEGIN_TM, WKDAY_OPERT_END_TM, CHRG_INFO, CONTCT_NO, SPCLABLT_MATR, SETTLE_METH))

    # 필터링된 주차장 정보 표시
    for i in range(len(DataList)):
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, i + 1)
        RenderText.insert(INSERT, "] ")
        RenderText.insert(INSERT, "주차장명: ")
        RenderText.insert(INSERT, DataList[i][0])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "주소: ")
        RenderText.insert(INSERT, DataList[i][1])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "주차구획수: ")
        RenderText.insert(INSERT, DataList[i][2])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "운영시간: ")
        RenderText.insert(INSERT, DataList[i][3])
        RenderText.insert(INSERT, " - ")
        RenderText.insert(INSERT, DataList[i][4])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "요금정보: ")
        RenderText.insert(INSERT, DataList[i][5])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "전화번호: ")
        RenderText.insert(INSERT, DataList[i][6])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "특이사항: ")
        RenderText.insert(INSERT, DataList[i][7])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "결제방법: ")
        RenderText.insert(INSERT, DataList[i][8])
        RenderText.insert(INSERT, "\n\n")

    RenderText.configure(state='disabled')
    SearchEntry.delete(0, END)

def InitRenderText():
    global RenderText

    text_frame = Frame(g_Tk)
    text_frame.pack()
    text_frame.place(x=10, y=150)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(text_frame, width=30, height=20, borderwidth=2, relief='ridge', font=TempFont)
    RenderText.pack(side=LEFT, fill=BOTH, expand=YES)

    RenderTextScrollbar = Scrollbar(text_frame, command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=Y)

    RenderText['yscrollcommand'] = RenderTextScrollbar.set

def InitSearchEntry():
    global SearchEntry
    Label(g_Tk, text="<검색할 시 이름>", fg="black", font=("Helvetica", 12)).place(x=10, y=90)
    SearchEntry = Entry(g_Tk, fg="black")
    SearchEntry.place(x=10, y=110)


def update_map():
    # 여기에 Google 지도 업데이트 코드 추가
    pass

InitTopText()
InitSearchEntry()
InitSearchButton()
InitRenderText()


g_Tk.mainloop()
