from flask import Flask, request, render_template, redirect, url_for, session
from mylib import *

app = Flask(__name__)
app.secret_key = 'hello'

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
        ID = request.form.get('ID')
        password = request.form.get('password')
        identity = request.form.get('identity')

        if identity == '学生':
            try:
                record = get_student_info(ID)
                user = Student(record)
                session['ID'] = ID
                session['identity'] = identity
                session['username'] = user.name
            except Exception as e:
                print(e)
                print("Fail to login as a student")
        elif identity == '管理员':
            try:
                record = get_admin_info(ID)
                user = Admin(record)
                session['ID'] = ID
                session['identity'] = identity
                session['username'] = user.name
            except Exception as e:
                print(e)
                print("Fail to login as an administrator")


        if ID == user.id and password == user.password and identity == '学生':
            session['state'] = 1
            return redirect(url_for('student_home'))
        elif ID == user.id and password == user.password and identity == '管理员':
            session['state'] = 1
            return redirect('/administrator_home')
        # 如果输错了 咋办 先不管他

    return render_template('login.html')


# 需要参数为username和identity，用以表示身份和姓名
@app.route('/student_home')
def student_home():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    return render_template('student_home.html', username=username, identity=identity)


# 需要学生类作为参数，包含学生的一切属性
@app.route('/student_file')
def student_file():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    ID = session['ID']

    record = get_student_info(ID)
    user = Student(record)

    with open("./static/image/student_head/"+ID+".jpg", 'wb') as f:
        f.write(user.photo)
    address = "./static/image/student_head/"+ID+".jpg"
    return render_template('student_file.html', username=username,
                           identity=identity, user=user, pic_address=address)


# 需要学生类？（给输入框初始值）
@app.route('/student_change', methods=['POST', 'GET'])
def student_change():
    if session['state'] is None:
        return redirect('/')
    ID = session['ID']
    username = session['username']
    identity = session['identity']

    if request.method == 'POST':
        # example
        cell_phone_number = request.form.get('cell_phone_number')
        email = request.form.get('email')
        password = request.form.get('password')
        photo = request.files.get('head')

        photo.save("stu_change_upload.jpg")
        with open("stu_change_upload.jpg", 'rb') as f:
            photo_data = f.read()
        update_student_info(ID, cell_phone_number, email, password, photo_data)

        record = get_student_info(ID)
        photo_data = record[-1]
        with open("./read.jpg", 'wb') as f:
            f.write(photo_data)

    return render_template('student_change.html', username=username, identity=identity)


# 需要参数为username和identity，用以表示身份和姓名
@app.route('/maintenance_request', methods=["POST", "GET"])
def maintenance_request():
    if session['state'] is None:
        return redirect('/')
    ID = session['ID']
    username = session['username']
    identity = session['identity']
    # TODO 表单提交的电话和维修区域在数据库中没有
    if request.method == 'POST':
        # example
        cell_phone_number = request.form.get('cell_phone_number')
        area = request.form.get('area')
        description = request.form.get('description')
        photo = request.files.get('pic')

        photo.save("maintain_upload.jpg")
        with open("maintain_upload.jpg", 'rb') as f:
            photo_data = f.read()

        report_maintenance(ID, description, photo_data)

    return render_template('maintenance_request.html', username=username, identity=identity)


# 示例用类
class Record_for_show:
    def __init__(self, time, reporter, status, address):
        self.content = "申请时间：" + str(time) + "  申请人：" + reporter + "  状态：" + status
        self.address = address


# 需要一个维修类的list,如果是学生查看，只显示自己宿舍的。如果是管理员查看，则显示全部；username和identity，用以表示身份和姓名
# 传入的数据需要有两个属性：1.想要显示的数据‘日期 申请人 状态’ 2.在table中的编号
@app.route('/maintenance_show')
def maintenance_show():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    ID = session['ID']

    records_for_show = []        # 这个列表里存放 Record_for_show 类
    if identity == "学生":
        records = get_stu_view_records(ID)      # records 是完整的记录列表, 其中存放Record类
        for record in records:
            tmp = Record_for_show(record.report_time, record.reporter_name, record.status, record.id)
            records_for_show.append(tmp)

    elif identity == "管理员":
        records = get_admin_view_records()  # records 是完整的记录列表, 其中存放Record类
        for record in records:
            tmp = Record_for_show(record.report_time, record.reporter_name, record.status, record.id)
            records_for_show.append(tmp)

    return render_template('maintenance_show.html', username=username, identity=identity, records=records_for_show)


# 查看第index个维修记录，因此需要第index个维修类
# 如果是管理员，则还要处理上传的修改状态
@app.route('/maintenance_detail/<int:index>', methods=['GET', 'POST'])
def maintenance_detail(index):
    if index < 0:
        return redirect('/maintenance_show')
    if session['state'] is None:
        return redirect('/')

    username = session['username']
    identity = session['identity']
    ID = session['ID']

    record = get_single_record(index)
    # TODO record 中存储了读出的Record类，类定义见mylib.py
    #  将record中的信息展示在detail界面中（已经展示维修状态作为测试）

    # TODO detail界面中的 联系方式和维修位置 在Maintenance数据库中没有，
    #  如果要单独select会破坏Record类的结构，那样会很丑陋

    if request.method == 'POST':
        # TODO update失败，button没效果？
        print(1)
        finish_record(index)
        return redirect('/maintenance_show')

    return render_template('maintenance_detail.html', username=username, identity=identity, record=record)


@app.route('/return_school_apply', methods=['POST', 'GET'])
def return_school_apply():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    ID = session['ID']
    # TODO 数据库的apply_for_return函数有问题
    if request.method == 'POST':
        description = request.form.get('description')
        apply_for_return(ID, description)

        return redirect('/student_home')

    return render_template('return_school_apply.html', username=username, identity=identity)


@app.route('/leave_school_apply', methods=['POST', 'GET'])
def leave_school_apply():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    ID = session['ID']

    # TODO 网页上的表单和数据库table表项不一致
    #  数据库：预期离开时间，目的地，描述； 网页：联系人，电话，描述
    # TODO 通过 request.form.get 函数获取数据 然后存到数据库中
    if request.method == 'POST':
        # example
        description = request.form.get('description')
        print(description)
        return redirect('/student_home')

    return render_template('leave_school_apply.html', username=username, identity=identity)


@app.route('/administrator_home')
def administrator_home():
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
        record = Record_for_show(i, i)
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
        record = Record_for_show(i, i)
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
        record = Record_for_show(i, i)
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
        record = Record_for_show(i, i)
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

