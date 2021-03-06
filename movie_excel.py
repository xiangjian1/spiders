
# -*- coding: UTF-8 -*-

# 设置编码格式为utf-8，为了可以打印出中文字符
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib2
from bs4 import BeautifulSoup
import xlwt

# 通过url得到页面全部内容
def get_url_content(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    return html

# 通过xlwt设置utf编码格式，并返回一个excel对象'book'
book=xlwt.Workbook(encoding='utf-8',style_compression=0)

# 新建一个sheet表
sheet=book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
# 给这个sheet添加4列名称
sheet.write(0,0,'电影详情url')
sheet.write(0,1,'电影图片url')
sheet.write(0,2,'电影中文名')
sheet.write(0,3,'电影简介')

# 定义一个全局的行数n，为了下面parser_to_excel方法写入excel时可以找到从哪一行开始写入
n=1

# 通过BeautifulSoup解析后的结构来获取内容，并存入excel
def parser_to_excel(soup):
    # 查看网页可以看到我们要获取的信息都在class='grid_view'里面，所以获取到它，再获取到其中所有的li标签，组成一个list
    content_list = soup.find(class_='grid_view').find_all('li')
    # 循环li标签列表
    for film_item in content_list:
        # 因为通过查看网页，可以看见一个电影节点里只有两个a标签，一个是图片链接，一个是名称链接
        # 所以这里通过第一个a标签获取电影详情url和电影图片pic地址
        film_detail_url = film_item.find_all('a')[0].get('href')
        film_pic = film_item.find_all('a')[0].find('img').get('src')

        # 可以看到，节点中有两个class='title'的标签，一个是电影的中文名称，一个是英文名称，这里我们取第一个就好
        film_name = film_item.find_all(class_='title')[0].text

        # 可以看到，节点中有一个class='inq'的标签，里面的内容是一句话简介，我们通过class获取就好
        # 因为第150个电影没有简介，所以这里用if处理一下，不然会抛异常
        if film_item.find(class_='inq') != None:
            film_quote = film_item.find(class_='inq').text

        # 好了，就先获取这些信息，现在把爬到的信息打印一下
        print ("正在爬取的信息如下：电影详情："+film_detail_url+"，电影图片："+film_pic+"，电影中文名："+film_name+"，电影简介："+film_quote)

        # 接下来就把这些信息存入excel
        global n
        sheet.write(n,0,film_detail_url)#往第n行，弟0列写入详情url信息，下同
        sheet.write(n,1,film_pic)
        sheet.write(n,2,film_name)
        sheet.write(n,3,film_quote)
        # 每次存入把n+1,代表下一次从下一行开始写
        print("正往第"+str(n)+"行写入数据")
        # 每次循环完，行数+1
        n=n+1

if __name__ == "__main__":

    base_url = 'https://movie.douban.com/top250'
    content = get_url_content(base_url)
    soup = BeautifulSoup(content, 'html.parser')
    # 获取当前页的信息并存入excel
    parser_to_excel(soup)

    # 获取其他要爬取的url地址
    # 可以通过按f12看到分页的代码写在class='paginator'里
    # 所以我们先获取到class=‘paginator’的div
    paginator_div = soup.find(class_='paginator')

    # 再获取div中所有的a标签，并循环获取到其中的href(跳转链接)，拼接url后逐个爬取
    for link in paginator_div.find_all('a'):
        # 因为href里都是"?start=25&amp;filter="这种形式，缺少网页前缀，所以拼接一下
        other_url = base_url+link.get('href')

        print("正在爬取url:"+other_url)

        # 同上，获取到其他网页的内容
        other_url_content = get_url_content(other_url)

        # 同上，获取到内容后通过BeautifulSoup，解析
        other_url_soup = BeautifulSoup(other_url_content, 'html.parser')

        #把分页里的2,3...等页里面的信息解析并存入excel
        parser_to_excel(other_url_soup)

    book.save(u'豆瓣电影Top250.xlsx')#保存
