import requests
import re
import json
from bs4 import BeautifulSoup
import pandas as pd
  
# 起始页
base_url = 'https://movie.douban.com/top250?start='

# 创建正则表达式对象，即对于我们要找的东西给出一个规则
# 返回的都为（）内部的内容。

find_link = re.compile(r'<a href="(.*?)">')
find_img = re.compile(r'<img.*src="(.*?)"', re.S) #re.S表示忽略换行符
find_title = re.compile(r'<span class="title">(.*)</span>')
find_rating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
find_person_cnt = re.compile(r'<span>(\d*人评价)</span>')
find_inq = re.compile(r'<span class="inq">(.*)</span>')
find_bd = re.compile(r'<p class="">(.*)</p>', re.S)

def ask_url(url):
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
   
    # 主要是这里与 urllib 有所不同
    resp = requests.get(url, headers=head ,timeout=30) 
    text = resp.text
    return text
  
  def get_data(base_url):
    print('get data')
    data_list = []
    
    for i in range(2):
        url = base_url + str(i*25)
        html = ask_url(url) 
        bs = BeautifulSoup(html, 'html.parser')
        
        for item in bs.find_all('div', class_='item'): 
            
            data = [] 
            item = str(item) 
            
            link = re.findall(find_link, item)[0] 
            data.append(link)
           
            img = re.findall(find_img, item)[0]
            data.append(img)
            
            title = re.findall(find_title, item)[0]
            data.append(title)
            
            rating = re.findall(find_rating, item)[0]
            data.append(rating)
            
            person_cnt = re.findall(find_person_cnt, item)[0]
            data.append(person_cnt)
            
            inq = re.findall(find_inq, item)[0]
            data.append(inq)
            
            bd = re.findall(find_bd, item)[0]
            data.append(bd)
            
            data_list.append(data)
            
    return data_list
  
datalist  = get_data(base_url)
output_data = pd.DataFrame(datalist)
