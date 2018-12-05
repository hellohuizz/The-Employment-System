import pymysql
class ConMysql:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',port=3306,db='Job',user='root',passwd='123456',charset='utf8')



    #params传进一个列表
    def insert_data(self, params):
        self.cur = self.conn.cursor()

        sql = 'insert into webpro_jobinfo(jobname, salary, workingExp, eduLevel, company_name,position, city_name,update_time,web_name,hash_id,job_require) values(%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)'
        self.cur.execute(sql,params)

        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

