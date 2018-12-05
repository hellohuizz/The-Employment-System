import hashlib

import requests
import time
import random

headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'25',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'_ga=GA1.2.1178060415.1542891838; user_trace_token=20181122210359-13b225a0-ee57-11e8-b514-525400f775ce; LGUID=20181122210359-13b22a32-ee57-11e8-b514-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221673b852ae1587-09bf574901d349-5c10301c-1049088-1673b852ae2143%22%2C%22%24device_id%22%3A%221673b852ae1587-09bf574901d349-5c10301c-1049088-1673b852ae2143%22%7D; index_location_city=%E5%8C%97%E4%BA%AC; WEBTJ-ID=20181127181405-16754a960a377d-0922d875ac6983-5c10301c-1049088-16754a960a54bb; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542891837,1542891871,1542891876,1543313646; X_HTTP_TOKEN=d645bb7ac19fe33851df1fc17d5564cc; ab_test_random_num=0; _putrc=CC217B0DD04C1A2D123F89F2B170EADC; JSESSIONID=ABAAABAAAIAACBI26B02761DD65761E87BB6418D966C90C; login=true; hasDeliver=0; TG-TRACK-CODE=search_code; LGSID=20181127213448-35af4547-f249-11e8-81a2-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fcity%3D%25E5%258C%2597%25E4%25BA%25AC%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; _gat=1; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B70562; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; gate_login_token=b7704ce17a8b555c1556bb27e333dbe7c046ba2bdb953f8e79cf8d51dd747a16; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543326807; LGRID=20181127215331-d32b738b-f24b-11e8-81a5-525400f775ce; SEARCH_ID=19051d309a954063b73343ebb58e816d',
    'Host':'www.lagou.com',
    'Origin':'https://www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_python?px=default&city=%E5%8C%97%E4%BA%AC',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'X-Anit-Forge-Code':'0',
    'X-Anit-Forge-Token':'None',
    'X-Requested-With':'XMLHttpRequest'
}

def get_data_info(url,datas,city,db,col):
    response = requests.post(url, data=datas, headers=headers)
    # print(type(response))
    # exit()
    # 获取工作列表的json数据
    page_json_data = response.json()['content']['positionResult']['result']
    # 遍历工作列表
    for p in page_json_data:
        city_name = city
        jobname = p['positionName']
        workingExp = p['workYear']
        eduLevel = p['education']
        update_time = p['createTime']
        position = p['city']
        salary = p['salary']
        company_name = p['companyFullName']
        sha1 = hashlib.sha1()
        string = (company_name + '' + update_time)
        stri = string.encode('utf8')
        sha1.update(stri)
        hash_id = sha1.hexdigest()
        item = {
            'jobname': jobname,
            'workingExp': workingExp,
            'eduLevel': eduLevel,
            'update_time': update_time,
            'position': position,
            'salary': salary,
            'company_name': company_name,
            'hash_id': hash_id,
            'city_name': city_name,
        }
        if city_name in col:
            result = db[city].find({'hash_id': item['hash_id']}).count()
            if result > 0:
                pass
            else:
                db[city].insert(item)
        else:
            col = db[city]
            col.insert(item)


import pymongo
def connect_mongodb():
    client = pymongo.MongoClient(host='localhost',port=27017)
    return client

def main():
    # 查询关键字
    keyword = input("请输入关键字：")

    city = input("请输入城市:")
    # 访问页数
    page = int(input("请输入要爬取的页数："))
    #访问路径
    url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(city)

    client = connect_mongodb()
    db = client.lagou
    col = db.list_collection_names()
    for n in range(page):
        # 拼接请求数据
        datas = {
            'first': 'true',
            'kd': keyword,
            'pn': str(n+1) # 页数
        }
        #调用获取数据方法
        get_data_info(url,datas,city,db,col)

        #短暂睡眠，防止反爬
        time.sleep(random.random())

if __name__ == '__main__':
    main()