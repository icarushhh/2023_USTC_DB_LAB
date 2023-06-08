from flask import Flask, request, render_template, redirect, url_for, session

import pymysql  # 引入pymssql模块

server = "localhost"  # 服务器名
user = "root"  # 用户名
password = ""  # 密码
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
# 传入的数据需要有两个属性：1.想要显示的数据‘日期 申请人 维修区域 状态’ 2.在list中的编号
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


# TODO 改成维修类的变量
status = 0


# 查看第index个维修记录，因此需要第index个维修类
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
    #  status表维修状态，在此用于演示
    global status
    # 表示已经维修完成
    if request.method == 'POST':
        # TODO 修改维修状态为已经完成 并传回数据库
        status = 1
        print(status)
        return redirect('/maintenance_show')

    username = session['username']
    identity = session['identity']

    return render_template('maintenance_detail.html', username=username, identity=identity, status=status)


@app.route('/return_school_apply', methods=['POST', 'GET'])
def return_school_apply():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    if request.method == 'POST':
        # example
        description = request.form.get('description')
        print(description)
        return redirect('/student_home')

    username = session['username']
    identity = session['identity']
    return render_template('return_school_apply.html', username=username, identity=identity)


@app.route('/leave_school_apply', methods=['POST', 'GET'])
def leave_school_apply():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')

    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    if request.method == 'POST':
        # example
        description = request.form.get('description')
        print(description)
        return redirect('/student_home')

    username = session['username']
    identity = session['identity']
    return render_template('leave_school_apply.html', username=username, identity=identity)


@app.route('/administrator_home')
def administrator_home():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    return render_template('administrator_home.html', username=username, identity=identity)


@app.route('/IO_school_manage', methods=['POST', 'GET'])
def IO_school_manage():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')

    username = session['username']
    identity = session['identity']
    return render_template('IO_school_manage.html', username=username, identity=identity)


# 用于处理入宿申请
@app.route('/In_school', methods=['POST'])
def In_school():
    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    name = request.form.get('name')
    print('In' + name)
    return redirect('/IO_school_manage')


# 用于处理离宿申请
@app.route('/Out_school', methods=['POST'])
def Out_school():
    # TODO 通过 request.form.get 函数获取数据 然后删除数据库中对应数据
    ID = request.form.get('ID_out')
    print('Out' + ID)
    return redirect('/IO_school_manage')


# TODO 需要两个list 一个是返校申请的list 一个是离校申请的list
@app.route('/LR_school_manage', methods=['POST', 'GET'])
def LR_school_manage():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # 演示用
    records = []
    for i in range(0, 50):
        record = Record(i, i)
        records.append(record)

    username = session['username']
    identity = session['identity']
    return render_template('LR_school_manage.html', username=username, identity=identity,
                           records1=records[:50], records2=records[50:])


# 查看第index个暂离申请，因此需要第index个暂离申请类
# 还要处理上传的修改状态
@app.route('/leave_school_detail/<int:index>', methods=['GET', 'POST'])
def leave_school_detail(index):
    # TODO 若维修list不存在，index小于0或大于维修list的长度，则返回LR_school_manage界面
    if index < 0:
        return redirect('/LR_school_manage')

    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过index获取指定维修记录，并传入render_template

    username = session['username']
    identity = session['identity']

    return render_template('leave_school_detail.html', username=username, identity=identity,
                           index=index)


# 用于通过离校申请
@app.route('/agree_leave_school/<int:index>', methods=['POST'])
def agree_leave_school(index):
    # TODO 将第index个暂离申请的状态改为通过
    print('agree_leave_school')
    return redirect('/LR_school_manage')


# 用于不通过离校申请
@app.route('/disagree_leave_school/<int:index>', methods=['POST'])
def disagree_leave_school(index):
    # TODO 将第index个暂离申请的状态改为不通过
    print('disagree_leave_school')
    return redirect('/LR_school_manage')


# 查看第index个返校申请，因此需要第index个返校申请类
# 还要处理上传的修改状态
@app.route('/return_school_detail/<int:index>', methods=['GET', 'POST'])
def return_school_detail(index):
    # TODO 若维修list不存在，index小于0或大于维修list的长度，则返回LR_school_manage界面
    if index < 0:
        return redirect('/LR_school_manage')

    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过index获取指定维修记录，并传入render_template

    username = session['username']
    identity = session['identity']

    return render_template('return_school_detail.html', username=username
                           , identity=identity, index=index)


# 用于通过返校申请
@app.route('/agree_return_school/<int:index>', methods=['POST'])
def agree_return_school(index):
    # TODO 将第index个返校申请的状态改为通过
    print('agree_return_school')
    return redirect('/LR_school_manage')


# 用于不通过返校申请
@app.route('/disagree_leave_school/<int:index>', methods=['POST'])
def disagree_return_school(index):
    # TODO 将第index个返校申请的状态改为不通过
    print('disagree_return_school')
    return redirect('/LR_school_manage')


# 需要管理员类（给输入框初始值）
@app.route('/administrator_change', methods=['POST', 'GET'])
def administrator_change():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    #  request.files.get 用以获取文件
    if request.method == 'POST':
        # example
        cell_phone_number = request.form.get('cell_phone_number')
        head = request.files.get('head')
        print(cell_phone_number)
        return redirect('/administrator_file')

    username = session['username']
    identity = session['identity']
    return render_template('administrator_change.html', username=username, identity=identity)


# 管理员修改学生数据 应该传入修改的哪个学生
# 改成学号会更好一点吗？
@app.route('/admin_change_student/<int:index>', methods=['POST', 'GET'])
def admin_change_student(index):
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中 注意如何获取修改的是哪个学生
    #  通过学号或者index来确定修改的哪个学生
    if request.method == 'POST':
        # example
        cell_phone_number = request.form.get('cell_phone_number')
        return redirect('/student_show')

    username = session['username']
    identity = session['identity']
    return render_template('admin_change_student.html', username=username, identity=identity)


# TODO 需要一个学生类的list
@app.route('/student_show', methods=['POST', 'GET'])
def student_show():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # 演示用
    records = []
    for i in range(0, 50):
        record = Record(i, i)
        records.append(record)

    username = session['username']
    identity = session['identity']
    return render_template('student_show.html', username=username, identity=identity,
                           records=records[:50])


# TODO 需要一个访客list
@app.route('/guest_show')
def guest_show():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # 演示用
    records = []
    for i in range(0, 50):
        record = Record(i, i)
        records.append(record)

    username = session['username']
    identity = session['identity']
    return render_template('guest_show.html', username=username, identity=identity,
                           records=records[:50])


# 查看第index个访客，因此需要第index个访客类
@app.route('/guest_detail/<int:index>', methods=['GET', 'POST'])
def guest_detail(index):
    # TODO 若list不存在，index小于0或大于维修list的长度，则返回LR_school_manage界面
    if index < 0:
        return redirect('/LR_school_manage')

    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过index获取指定访客记录，并传入render_template

    username = session['username']
    identity = session['identity']

    return render_template('guest_detail.html', username=username, identity=identity, index=index)


# 处理登记访客
@app.route('/guest_register', methods=['POST', 'GET'])
def guest_register():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')

    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    if request.method == 'POST':
        # example
        description = request.form.get('description')
        print(description)
        return redirect('/guest_show')

    username = session['username']
    identity = session['identity']
    return render_template('guest_register.html', username=username, identity=identity)


# 处理修改访客
@app.route('/guest_change/<int:index>', methods=['POST', 'GET'])
def guest_change(index):
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')

    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    if request.method == 'POST':
        # example
        description = request.form.get('description')
        print(description)
        return redirect('/guest_show')

    username = session['username']
    identity = session['identity']
    return render_template('guest_change.html', username=username, identity=identity)


# TODO 需要一个宿舍类的list
@app.route('/room_show', methods=['POST', 'GET'])
def room_show():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # 演示用
    records = []
    for i in range(0, 50):
        record = Record(i, i)
        records.append(record)

    username = session['username']
    identity = session['identity']
    return render_template('room_show.html', username=username, identity=identity,
                           records=records[:50])


# 查看第index个宿舍，因此需要第index个宿舍类
@app.route('/room_detail/<int:index>', methods=['GET', 'POST'])
def room_detail(index):
    # TODO 若list不存在，index小于0或大于list的长度，则返回界面
    if index < 0:
        return redirect('/room_show')

    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')
    # TODO 通过index获取指定访客记录，并传入render_template

    username = session['username']
    identity = session['identity']

    return render_template('room_detail.html', username=username
                           , identity=identity, index=index)


# 处理修改房间
@app.route('/room_change/<int:index>', methods=['POST', 'GET'])
def room_change(index):
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')

    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    if request.method == 'POST':
        # example
        description = request.form.get('description')
        print(description)
        return redirect('/room_show')

    username = session['username']
    identity = session['identity']
    return render_template('room_change.html', username=username, identity=identity)


@app.route('/administrator_file')
def administrator_file():
    # TODO state表示是否已经登录
    if session['state'] is None:
        return redirect('/')

    username = session['username']
    identity = session['identity']
    return render_template('administrator_file.html', username=username, identity=identity)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
