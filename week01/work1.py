import requests
from bs4 import BeautifulSoup as bs
import lxml.etree
import pandas as pd

url='https://maoyan.com/board/4'
header={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'}

#找到所有电影主页
def pageAll(url,header):
    home=requests.get(url,headers=header)
    pages=[]
    bs_info=bs(home.text,'html.parser')
    for tag in bs_info.find_all('a',attrs={'class':'image-link'}): #注意 attrs
        atag='https://maoyan.com'+tag.get('href')
        pages.append(atag)
    return pages


#lxml化
pages=pageAll(url,header)
films=[]
for page in pages:
    response=requests.get(page,headers=header)
    print(response.status_code)
    selector=lxml.etree.HTML(response.text)
    #电影信息
    film_name=selector.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')
    types=selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a/text()')
    film_date=selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')
    mylist={'电影名称':film_name,'电影类型':types,'上映日期':film_date}
    print(mylist)
    films.append(mylist)

#panda保存
movies=pd.DataFrame(films,columns=['电影名称','电影类型','上映日期'])
movies.to_csv('./movies.csv',encoding='gbk',index=False)