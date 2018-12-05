import time

from goData.client_mongodb import ConMongodb
from goData.client_myql import ConMysql

def match_field(data):
    company_name = data['company_name']
    eduLevel = data['eduLevel']
    jobname = data['jobname']
    position = data['position']
    salary = data['salary']
    city_name = data['city_name']
    hash_id = data['hash_id']
    jobrequire= data['job_require']
    if len(jobrequire)>800:
        jobrequire = jobrequire[:500]

    job_require = jobrequire
    update_time = data['update_time']
    workingExp = data['workingExp']
    web_name = '智联招聘'
    params = [jobname, salary, workingExp, eduLevel, company_name, position, city_name, update_time, web_name, hash_id,
              job_require]

    return params

def main():
    mondb = ConMongodb()
    mondb.con_collection('Job','zhilian')
    mysdb = ConMysql()

    #拿到mongodb里的数据
    data_list=mondb.read_data()

    time.sleep(10)
    i =1

    for data in data_list:

        print(i)
        i+=1
        try:

            params = match_field(data)
            # print(params)
            mysdb.insert_data(params)
        except Exception as e:
            print(e)
            continue

    mysdb.close()





if __name__ == '__main__':
    main()