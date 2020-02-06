import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

# 웹사이트에 접근해서 크롤링 할때 권한 받을수 있음 - User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

#변수로 url담으면 관리 용이함
url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20191102'
data = requests.get(url, headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

rank = 1
music_data = {
    'rank': rank,
    'image':'',
    'title':'',
    'artist':''
}

for music in musics:
    title = str(music.select_one('td.info > a.title.ellipsis').text).strip()
    # td.info > a.title or td > a.title도 같은 결과 출력되지만 경로를 정확하게 하는게 좋
    print(title)

    artist = str(music.select_one('td.info > a.artist.ellipsis').text)
    print(artist)

    image = 'https:' + str(music.select_one('img').attrs['src'])
    # image = str(music.select_one('img').attrs['src']).replace('//','') 알려주신 방
    # output //image.genie.co.kr/Y/IMAGE/IMG_ALBUM/081/297/613/81297613_1574066356132_1_140x140.JPG
    print(image)


    music_data = {
        'rank': rank,
        'image':image,
        'title': title,
        'artist': artist
    }
    db.musics.insert_one(music_data)#db에 data넣기
    rank += 1