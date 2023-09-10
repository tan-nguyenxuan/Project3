list=['xe']
import requests 
from bs4 import BeautifulSoup

for tmp1 in list:
    check=0
    dem=0
    data=[]
    links=[]
    for tmp2 in range(1,350):
        tmp3= ("https://tuoitre.vn/") + tmp1 + '/trang-' + str(tmp2) +'.htm'
        response=requests.get(tmp3)
        print(tmp3)
        soup = BeautifulSoup(response.content, "html.parser")
        if soup.findAll('h3', class_='box-title-text') is not None:
            titles = soup.findAll('h3', class_='box-title-text')
        else :
            if soup.findAll('h2', class_='box-title-text') is not None:
                titles = soup.findAll('h2', class_='box-title-text')
            else :
                titles = soup.findAll('h1', class_='box-title-text')
        links = [link.find('a').attrs["href"] for link in titles]
        for link in links:
            print(link)
            news = requests.get('https://tuoitre.vn/'+link)
            soup = BeautifulSoup(news.content, "html.parser")
            try:
                topic = soup.select_one('#main-detail > div.detail-top > div.detail-cate > a').text
                if topic != "Xe":
                    continue
            except:
                continue
            content = soup.select('#main-detail > div.detail-cmain > div > p')
            if dem==11000:
                check=1
                break;
            if content is not None:
                path_w='data1/datatest/' + tmp1 + '/' + str(dem) +'.txt'
                print(path_w)
                with open(path_w, mode='w',encoding = "utf-8") as f:
                    for a in content:
                        f.write(a.text + '\n')
                f.close()
                dem=dem+1
            else:
                continue
        if check==1:
            print(dem)
            break
        