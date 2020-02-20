import requests
from bs4 import BeautifulSoup
import json

def getHtml(url,headers):
    try:
        r = requests.get(url,headers = headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print('爬取失败')
        return ''

def htmlParser(html):
    try:
        id_list = []
        soup = BeautifulSoup(html,'html.parser')
        li = soup.select('.f-hide li a')
        for i in li:
            id_list.append(i['href'].split('=')[-1])

        return id_list
    except:
        print('获得id出错')
        return ''

def get_name_singer(html):
    name_sig_list = []
    soup = BeautifulSoup(html,'html.parser')
    name = soup.select('.f-ff2')
    singer = soup.select('p.des.s-fc4 span a')
    name_sig_list.append(name[0].text)
    name_sig_list.append(singer[0].text)
    return name_sig_list
def getMusic(lst,nslst):
        filename = "regebang.json"
        urls = []
        info = [{"num": "排名", "href": "", "name": "歌曲名", "singer": "歌手"}]
        for id in lst:
            urls.append('http://music.163.com/song?id=' + id)
        for i in range(len(urls)):
            info.append({"num": (i + 1), "href": urls[i], "name": nslst[i][0], "singer": nslst[i][1]})

        try:
            with open(filename, "w") as fp:
                fp.write(json.dumps(info))
                fp.close()
                print('下载成功')

        except:
            print('下载失败')





def main():
    urlls = []
    name_singer_list = []
    url = 'https://music.163.com/discover/toplist?id=3778678'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    html = getHtml(url,headers)
    idlist = htmlParser(html)
    for id in idlist:
        urlls.append('https://music.163.com/song?id='+id)
    for url in urlls:
        html = getHtml(url,headers)
        name_singer_list.append(get_name_singer(html))
     #print(name_singer_list)
    getMusic(idlist,name_singer_list)
main()

