from bs4 import BeautifulSoup
import requests
import sys

city = sys.argv[1]
area = sys.argv[2]
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

def weather(city, area):
  #===Preprocess===
  respond = requests.get(f"https://www.msn.com/zh-tw/weather/hourlyforecast/in-{area}, {city}", headers= headers)
  
  today_soup = BeautifulSoup(respond.text, "html.parser")
  #===Getting data===
  
  temp = today_soup.find(class_ = "firstLineText-DS-XwdBJw").string

  print(f"https://www.msn.com/zh-tw/weather/hourlyforecast/in-{area}, {city}")
  #print(respond.text)

  weather_status = {"縣市": city, "鄉鎮市區": area, "溫度": temp,
                    "降雨機率": f"{int}%", "未來三小時溫度": int, "紫外線指數": int,
                    "一周預報": list, "空氣品質": str, "明天溫度(同個時間點)": int}
  
  return weather_status

if __name__ == "__main__":
  #weather(city, area)
  print(weather(city, area))