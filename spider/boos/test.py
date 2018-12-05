import hashlib
import time

import requests
from lxml import etree


def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    url = 'https://www.zhipin.com/job_detail/?query=python&scity=101010100&industry=&position='
    r = requests.get(url=url, headers=headers)
    tree = etree.HTML(r.content)
    a_list = tree.xpath('//*[@id="main"]/div/div[3]/ul/li/div/div[1]/h3/a/@href')
    item = {}
    for a in a_list:
        a_href = 'https://www.zhipin.com' + a
        r1 = requests.get(a_href, headers=headers)
        response = etree.HTML(r1.content)
        # # 职位
        name = response.xpath('//div[@class="info-primary"]/div[@class="name"]/h1/text()')[0]
        item['name'] = name
        # 薪资
        salary = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()')[0].replace('\n', '').strip()
        item['salary'] = salary
        # 地点
        result = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/p/text()')
        place = result[0]
        item['place'] = place
        # # 经验
        experience = result[1]
        item['experience'] = experience
        # 学历
        Education = result[2]
        item['Education'] = Education
        # # 公司
        company = response.xpath('//*[@id="main"]/div[1]/div/div/div[3]/h3/a/text()')[0]
        item['company'] = company
        # 发布时间
        push_time = response.xpath('//span[@class="time"]/text()')[0]
        item['push_time'] = push_time
        # 任职要求
        job_requirements = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[3]/div[1]/div/text()')
        job_requirement = ''
        for i in job_requirements:
            job_requirement += i.replace('\u2028', '').strip()

        item['job_requirements'] = job_requirement
        # 根据上传字段生成hash值
        sha1 = hashlib.sha1()
        string = str(company + push_time + name + Education + experience + place + salary + job_requirement)
        stri = string.encode('utf8')
        sha1.update(stri)
        item['hash_id'] = sha1.hexdigest()
        time.sleep(1)
        print(item)


# if __name__ == '__main__':
    # main()
def s():
    s = '\xe5'
    print(s.strip('\xe5'))
if __name__ == '__main__':
    s()