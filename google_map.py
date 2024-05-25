import requests
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
from googlemaps import Client
import hdy_main
Google_API_Key = 'AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE'
gmaps = Client(key=Google_API_Key)
def update_map(city_name):
    global zoom
    city_center = gmaps.geocode(f"{city_name} 경기도")[0]['geometry']['location']
    city_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={city_center['lat']},{city_center['lng']}&zoom=13&size=400x400&maptype=roadmap"

    # 선택한 시의 주차장 위치 마커 추가
    for _, _, _, _, lat, lng in hdy_main.DataList:
        if lat and lng:
            city_map_url += f"&markers=color:red%7C{lat},{lng}"

    city_map_url += f"&key={Google_API_Key}"

    response = requests.get(city_map_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = ImageTk.PhotoImage(img)

    map_label = Label(hdy_main.g_Tk, width=300, height=300, bg='white')
    map_label.pack()
    map_label.place(x=270, y=45)
    map_label.configure(image=img)
    map_label.image = img