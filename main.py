from flask import Flask, request, render_template, redirect, url_for, session

import pymysql  # 引入pymssql模块

server = "localhost"  # 服务器名
user = "root"  # 用户名
password = "ZSZ1103753519123"  # 密码
database = "Lab1"  # 数据库名

connection = pymysql.connect(host=server,
                             user=user,
                             password=password,
                             database=database)  # 建立连接

cursor = connection.cursor()  # 创建游标对象

# 查询语句
sql = "SELECT * FROM Book where ID = 'b1'"  # test表格为自建表格，及填充相关内容

try:
    cursor.execute(sql)  # 执行查询语句
    results = cursor.fetchall()  # 获取所有记录列表
    print(results)
except:
    print("查询失败")

connection.close()  # 关闭数据库连接

app = Flask(__name__)
app.secret_key = 'hello'


# TODO 设计一个学生类

# TODO 设计一个管理员类

# TODO 设计一个维修类


# 初始化未登录
@app.before_request
def before_request():
    if 'state' not in session:
        session['state'] = None


# route括号中内容为该网页路径
@app.route('/', methods=['POST', 'GET'])
def login():
    # request.form.get用于在网页中获取数据，在点击submit按钮后触发(?)
    # 参数对应html文件中input框中的name

    if request.method == 'POST':
        # print(g.user_name)
        # TODO 在这里插入函数，判断输入的是否在数据库中，
        #  然后将用户资料传入session这个全局变量中,以便后续使用
        #  session是一个基于cookie保存的字典
        ID = request.form.get('ID')
        password = request.form.get('password')
        identity = request.form.get('identity')
        session['ID'] = ID
        session['password'] = password
        session['identity'] = identity
        session['username'] = '陈奕晓'

        # TODO 改成判断函数
        if ID == 'PB20111684' and password == 'As13771545222' and identity == '学生':
            # TODO 登录状态改为已登录
            session['state'] = 1
            return redirect(url_for('student_home'))
        elif ID == 'PB20111684' and password == 'As13771545222' and identity == '管理员':
            session['state'] = 1
            return redirect('/administrator_home')
        # 如果输错了 咋办 先不管他

    return render_template('login.html')


# 需要参数为username和identity，用以表示身份和姓名
@app.route('/student_home')
def student_home():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    return render_template('student_home.html', username=username, identity=identity)


# 需要学生类作为参数，包含学生的一切属性
@app.route('/student_file')
def student_file():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    return render_template('student_file.html', username=username, identity=identity)


# 需要学生类？（给输入框初始值）
@app.route('/student_change', methods=['POST', 'GET'])
def student_change():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    #  request.files.get 用以获取文件
    if request.method == 'POST':
        # example
        cell_phone_number = request.form.get('cell_phone_number')
        head = request.files.get('head')

    username = session['username']
    identity = session['identity']
    return render_template('student_change.html', username=username, identity=identity)


# 需要参数为username和identity，用以表示身份和姓名
@app.route('/maintenance_request')
def maintenance_request():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    #  request.files.get 用以获取文件
    if request.method == 'POST':
        # example
        cell_phone_number = request.form.get('cell_phone_number')
        head = request.files.get('head')

    username = session['username']
    identity = session['identity']
    return render_template('maintenance_request.html', username=username, identity=identity)


# 示例用类
class Record:
    def __init__(self, content, address):
        self.content = content
        self.address = address


# 需要一个维修类的list,如果是学生查看，只显示自己宿舍的。如果是管理员查看，则显示全部；username和identity，用以表示身份和姓名
@app.route('/maintenance_show')
def maintenance_show():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 写一个函数，要求：如果是学生查看，只显示自己宿舍的。如果是管理员查看，则显示全部
    #  返回符合要求的维修记录list,并存到全局变量session中去
    records = []
    for i in range(0, 50):
        record = Record(i, i)
        records.append(record)

    username = session['username']
    identity = session['identity']
    return render_template('maintenance_show.html', username=username, identity=identity, records=records)


# 查看第index个维修记录
# 如果是管理员，则还要处理上传的修改状态
@app.route('/maintenance_detail/<int:index>', methods=['GET', 'POST'])
def maintenance_detail(index):
    # TODO 若维修list不存在，index小于0或大于维修list的长度，则返回maintenance_show界面
    if index < 0:
        return redirect('/maintenance_show')

    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过index获取指定维修记录，并传入render_template
    status = 0
    # TODO 获取修改的状态
    if request.method == 'POST':
        # TODO 在这里将修改后的状态传回数据库
        status = request.json.get('status')
        print(status)

    username = session['username']
    identity = session['identity']

    return render_template('maintenance_detail.html', username=username, identity=identity, status=status)


@app.route('/administrator_home')
def administrator_home():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    return render_template('administrator_home.html', username=username, identity=identity)

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
