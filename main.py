from flask import Flask, request, render_template
import pymysql #引入pymssql模块

server = "localhost" #服务器名
user = "root" #用户名
password = "ZSZ1103753519123" #密码
database = "Lab1" #数据库名

connection = pymysql.connect(host=server,
                             user=user,
                             password=password,
                             database=database) #建立连接

cursor = connection.cursor() #创建游标对象

#查询语句
sql = "SELECT * FROM Book where ID = 'b1'" #test表格为自建表格，及填充相关内容

try:
    cursor.execute(sql) #执行查询语句
    results = cursor.fetchall() #获取所有记录列表
    print(results)
except:
    print("查询失败")

connection.close() #关闭数据库连接





app = Flask(__name__)


# 用于测试维修记录显示
class Record:
    def __init__(self, content, address):
        self.content = content
        self.address = address


# route括号中内容为该网页路径
@app.route('/')
def hello_world():

   # 调试，不用管
    records = []
    for i in range(0, 100):
        record = Record(str(i), str(i + 100))
        records.append(record)
    # render_template相当于调用html文件
    return render_template('login.html')
    # return  render_template('student_home.html', name='cyx')

    # return render_template('maintenance_show.html', recordmain.py
    # home.html
    # home_style.css
    # student_home_style.css
    # login_style.css
    # student_home.html
    # login.htmls=records)
    # return render_template('administrator_change.html')
    # return render_template('student_file.html')
    # return render_template('administrator_file.html')




# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run(debug=True)
