from bs4 import BeautifulSoup
import requests
import sys
from time import ctime

current_hour = int(ctime()[11: 13])
city = sys.argv[1]
area = sys.argv[2]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

def weather(city, area):
  #===Preprocess===
  respond = requests.get(f"https://www.msn.com/zh-tw/weather/hourlyforecast/in-{area}, {city}", headers= headers)
  
  soup = BeautifulSoup(respond.text, "html.parser")

  #===Getting data===
  
  raining_rate = str(soup.find_all(class_ = "rowItemText-DS-cwphqS")[5])
  raining_rate = raining_rate[raining_rate.index(">")+1 : raining_rate.index("%")+1]

  tomr_temp = str(soup.find_all(class_ = "rowItemText-DS-cwphqS")[4* (current_hour+(current_hour-24))])
  tomr_temp = tomr_temp[tomr_temp.index(">")+1: tomr_temp.index("°")+1]

  weather_status = {"縣市": city, "鄉鎮市區": area,
                    "溫度": soup.find(class_ = "firstLineText-DS-XwdBJw").string,
                    "降雨機率": raining_rate,
                    "未來三小時溫度": soup.find_all(class_ = "rowItemText-DS-cwphqS")[12].string,
                    "紫外線指數": int, #need to find another web site. pass
                    "一周預報": list,
                    "空氣品質": str, #need to find another web site. pass
                    "明天溫度(同個時間點)": tomr_temp
                    }
  
  return weather_status

if __name__ == "__main__":
  #weather(city, area)
  print(weather(city, area))