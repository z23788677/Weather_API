from bs4 import BeautifulSoup
import requests
import sys
from time import ctime
import json
import os

current_hour = int(ctime()[11: 13])
try:
  city = sys.argv[1]
  area = sys.argv[2]
except:
    print("API輸入錯誤，輸入如下: python main.py (縣市) (鄉鎮市區)\n 範例:python main.py 臺南市 北區")
    exit()

headers={'Content-type': 'text/plain; charset=utf-8'}

def weather(city, area):
  #===Preprocess===
  respond = requests.get(f"https://www.msn.com/zh-tw/weather/hourlyforecast/in-{area}, {city}", headers= headers)
  respond2 = requests.get(f"https://tw.news.yahoo.com/weather?location-picker={city}+{area}", headers= headers)
  
  soup = BeautifulSoup(respond.text, "html.parser")
  soup2 = BeautifulSoup(respond2.text, "html.parser")
  #===Getting data===
  
  raining_rate = (soup.find_all(class_ = "rowItemText-DS-cwphqS")[5]).text
  

  tomr_temp = str(soup.find_all(class_ = "rowItemText-DS-cwphqS")[4* (current_hour+(current_hour-24))])
  tomr_temp = tomr_temp[tomr_temp.index(">")+1: tomr_temp.index("°")+1]

  UV_index = soup2.find_all(class_ = "D(f) Py(8px) Bdb Bdbs(d) Bdbw(1px) Bdbc(t) Jc(sb)")[0].find("dd").text

  vision = soup2.find_all(class_ = "D(f) Py(8px) Bdb Bdbs(d) Bdbw(1px) Bdbc($weatherBorderColor) Jc(sb)")[-1].find_all("dd")[-1].text

  humidity = soup2.find_all(class_ = "D(f) Py(8px) Bdb Bdbs(d) Bdbw(1px) Bdbc($weatherBorderColor) Jc(sb)")[1].find("dd").text

  weather_status = {"縣市": city, "鄉鎮市區": area,
                    "溫度": soup.find(class_ = "firstLineText-DS-XwdBJw").string,
                    "降雨機率": raining_rate,
                    "未來三小時溫度": soup.find_all(class_ = "rowItemText-DS-cwphqS")[12].string,
                    "紫外線指數": UV_index,
                    "能見度": vision,
                    "濕度": humidity,
                    "明天溫度(同個時間點)": tomr_temp
                    }
  return weather_status

if __name__ == "__main__":
  output = w = json.dumps(weather(city, area), ensure_ascii=False, indent=4)
  json_path = open(f"{os.getcwd()}\\outcome.json", "w", encoding="utf8")
  json_path.write(output)
  json_path.close()
