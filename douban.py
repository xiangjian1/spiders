#coding:utf8
import urllib2, urllib,json

base_url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&'

headers = {
    "Host": "movie.douban.com",
    "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Referer": "https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action=",
    "Accept-Language": "zh-CN,zh;q=0.8",
}

if __name__ == '__main__':
    start = raw_input('输入电影开始：')
    end = raw_input('输入电影结束：')

    qs = {
        'start' : start,
        'limit' : str(int(end)-int(start) + 1),
    }
    fullurl = base_url + urllib.urlencode(qs)
    request = urllib2.Request(fullurl,headers=headers)
    response = urllib2.urlopen(fullurl)
    data_json = response.read()
    data = json.loads(data_json) #转成字典
    with open('douban.json', 'w') as f:
        # print type(json.dumps(data,indent=4,ensure_ascii=False))  # json.dumps 返回unicode字符集
        f.write(json.dumps(data,indent=4,ensure_ascii=False).encode('utf-8')) #写入文件时候需要转成utf-8
