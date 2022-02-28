#----------爬取豆瓣top250的电影信息-------------
from bs4 import BeautifulSoup #网页解析，获取数据
import re #正则表达式，进行文字匹配
from urllib import request, error #获取网页数据
import xlwt
import urllib
import pandas as pd

'''
BeautifulSoup4的四个重要接口：
BeautifulSoup4(bs4)可以把复制html文档转换为一个复杂的树形结构，每个节点都是python对象。所有对象可以归纳为4种：
-Tag: 标签及其内容，默认只拿到所找到的第一个内容
-NavigableString：标签里的内容，可以直接理解为字符串
-BeautifulSoup：表示整个文档。进行任何内容的访问都需要从整个文档的接口出发。
-Comment：是一个特殊的NavigableString，输出的内容不包含注释符号
'''

# 以豆瓣的top250的电影页面为例：
# 第一页：https://movie.douban.com/top250?start=   第二页：https://movie.douban.com/top250?start=25

# 第一页即起始页
base_url = 'https://movie.douban.com/top250?start='

# 创建正则表达式对象，即对于我们要找的东西给出一个规则，注意！！返回的都为（）内部的内容。
#影片链接
find_link = re.compile(r'<a href="(.*?)">')

#影片海报
find_img = re.compile(r'<img.*src="(.*?)"', re.S) #re.S表示忽略换行符

#影片片名
find_title = re.compile(r'<span class="title">(.*)</span>')

#影片评分
find_rating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')

#评价人数
find_person_cnt = re.compile(r'<span>(\d*人评价)</span>')

#影片概况
find_inq = re.compile(r'<span class="inq">(.*)</span>')

#影片的相关内容
find_bd = re.compile(r'<p class="">(.*)</p>', re.S)


# -------------------关键步骤：专门得到 “一个指定url” 的网页内容的函数----------------------
def ask_url(url):
    # 用户代理告诉要访问的服务器：我们是什么类型的机器，浏览器。本质上是告诉浏览器，我们可以接收什么水平的文件内容
    # 模拟浏览器头部信息向服务器发送消息
    head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    
    # 伪装请求对象
    req = request.Request(url = url, 
                          headers = head, #主要是这个，包含这个可以访问很多一般界面。要不没权限
                          # data=data, #注释掉一般也可以访问
                          # method='POST' #这里的模式为post请求，也可以为get请求
                         ) 
    # 超时处理
    try:
        resp = request.urlopen(req, timeout=30) #解析网页
        html = resp.read().decode('utf-8') #网页解码后的内容
        
        # 输出状态码
        print('status code:', resp.status)
        # 输出头部信息
        # print(resp.getheaders())
        # 输出解码后的内容
        # print(resp.read().decode('utf-8'))
        
    except error.URLError as e:
        # 打印出异常情况和异常原因
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
            
    return html
    
#--------------------------------主体框架 [获取数据 > 逐一解析 > 存储数据]---------------------------------
#[1] 定义获取数据的函数
def get_data(base_url):
    print('get data')
    data_list = []
    
    # 使用for循环定义一共获取几页的数据
    for i in range(2):
        url = base_url + str(i*25) #这里进针对于豆瓣top250的电影页面，每页包含25个电影
        html = ask_url(url) # 保存获取到的网页源码
    
        #[2] 逐一解析模块：需要写在for循环里
        bs = BeautifulSoup(html, 'html.parser')
        # 查找符合要求的字符串，返回列表
        # 注意！！这一块需要根据浏览器访问页面的代码。匹配到我们需要的信息，再提取对应的代码。这里规定了 class_ = 'item'，要不然会找出多余的内容。
        for item in bs.find_all('div', class_='item'): 
            
            data = [] #用于保存一部电影的所有信息
            item = str(item) #将内容转换为字符串
            
            #通过正则查找指定的字符串（这里用于找电影的链接）
            link = re.findall(find_link, item)[0] #这里加[0]是因为会同时找到两个相同的链接，返回第一个就够了
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


#[3] 定义保存数据的函数
def save_data(save_path):
  #暂不补充 
    print('save data')
    
#--------------运行主体框架的代码，获取数据------------------    
datalist  = get_data(base_url)

# 至此就得到我们所需要的文件。
output_data = pd.DataFrame(datalist)




#------------------------补充：BeautifulSoup进行解析时的各个模块作用--------------------------
bs = BeautifulSoup(html, 'html.parser')

# 打印整个文档的名字，内容
print(bs.name)
#print(bs)

# 打印不同模块
print(bs.title)
print(bs.a)
print(bs.head)

#打印类型
print(type(bs))
print(type(bs.head))

#打印标题文本
print(bs.title.string)

#打印属性
print(bs.title.attrs)

#打印内容文本和类型
print(bs.a.string)
print(type(bs.a.string)) # 输出为comment

#！！平时较为常用的有 bs本身，.string, .a 这三个




#------------------------补充：解析时的两个关键步骤：对于整个页面的内容，通过文档的【遍历】（拿所有的东西）和【搜索】（有针对性的拿东西）来获取指定的内容---------------------------
#【文档的遍历】：可以去网上搜索BeautifulSoup文档，里面有更多类似于contents的接口信息。
# 例如：
bs.head.contents #返回一个列表，包含了head中的各项内容

#【文档的搜索】：这个比较重要，经常用到
# [字符串过滤]

# 1 直接找所有含a标签的（注意这里只返回包含单个a标签的），返回一个列表
bs.find_all('a')

# 2 正则表达式搜索：使用search方法来匹配内容。（注意这里返回所有含a的内容）
bs.find_all(re.compile('a'))

# 3 使用方法来搜索：根据函数的要求来搜索
def name_is_exists(tag):
    return tag.has_attr('name')

bs.find_all(name_is_exists)

# [参数过滤]

# 4 指定参数进行搜索
bs.find_all(id='head') # 返回id=head下的所有内容，除了id还有其他的参数，这里不叙述

bs.find_all(text=['豆瓣','电影','导演']) # text参数可以接收列表，把列表内的内容搜索出来

bs.find_all('a', limit=3) # 通过limit限制返回3条数据

# [css选择器] 需要了解一些前端知识
bs.select('title') #按照标签来查找
bs.select('.mnav') #按照类名来查找
bs.select('#U1') #按照ID来查找
bs.select("a[class='bri']") #查找a标签中属性=bri的内容
bs.select('head > title') # 通过子标签查找，找到head里面的title内容

