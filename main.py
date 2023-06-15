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
            except:
                print("user name doesn't exist")
                return render_template('login.html')
        elif identity == '管理员':
            try:
                record = get_admin_info(ID)
                user = Admin(record)
                session['ID'] = ID
                session['identity'] = identity
                session['username'] = user.name
            except:
                print("user name doesn't exist")
                return render_template('login.html')
        else:
            return render_template('login.html')

        if ID == user.id and password == user.password and identity == '学生':
            session['state'] = 1
            return redirect(url_for('student_home'))
        elif ID == user.id and password == user.password and identity == '管理员':
            session['state'] = 1
            return redirect('/administrator_home')
        # 如果输错了 咋办 先不管他

    return render_template('login.html')


"""
======================================================== Student page =================================================
"""


# 需要参数为username和identity，用以表示身份和姓名
@app.route('/student_home')
def student_home():
    if session['state'] is None:
        return redirect('/')
    ID = session['ID']
    username = session['username']
    identity = session['identity']
    record = get_student_info(ID)
    user = Student(record)
    state = user.state

    return render_template('student_home.html', username=username,
                           identity=identity, state=state)


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

    try:
        with open("./static/image/student_head/" + ID + ".jpg", 'wb') as f:
            f.write(user.photo)
        address = "/static/image/student_head/" + ID + ".jpg"
    except Exception:
        address = ""

    return render_template('student_file.html', username=username,
                           identity=identity, user=user, address=address)


@app.route('/student_change', methods=['POST', 'GET'])
def student_change():
    if session['state'] is None:
        return redirect('/')
    ID = session['ID']
    username = session['username']
    identity = session['identity']

    record = get_student_info(ID)
    user = Student(record)

    if request.method == 'POST':
        # example
        cell_phone_number = request.form.get('cell_phone_number')
        email = request.form.get('email')
        password = request.form.get('password')
        photo = request.files.get('head')
        if photo.filename != '':
            photo.save("./static/image/student_head/" + ID + ".jpg")
            with open("./static/image/student_head/" + ID + ".jpg", 'rb') as f:
                photo_data = f.read()
        # 下为屎山代码 印度大厨
        else:
            # print('photo is none')
            with open("./static/image/student_head/" + ID + ".jpg", 'wb') as f:
                f.write(user.photo)
            with open("./static/image/student_head/" + ID + ".jpg", 'rb') as f:
                photo_data = f.read()

        update_student_info(ID, cell_phone_number, email, password, photo_data)

        return redirect('/student_file')

    return render_template('student_change.html', username=username
                           , identity=identity, user=user)


# 需要参数为username和identity，用以表示身份和姓名
@app.route('/maintenance_request', methods=["POST", "GET"])
def maintenance_request():
    if session['state'] is None:
        return redirect('/')
    ID = session['ID']
    username = session['username']
    identity = session['identity']

    if request.method == 'POST':
        # example
        description = request.form.get('description')
        photo = request.files.get('pic')

        photo.save("./tmp_maintenance.jpg")
        with open("./tmp_maintenance.jpg", 'rb') as f:
            photo_data = f.read()

        report_maintenance(ID, description, photo_data)

        return redirect('/student_home')

    return render_template('maintenance_request.html', username=username, identity=identity)


# 示例用类
class Maintenance_record_for_show:
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

    records_for_show = []  # 这个列表里存放 Record_for_show 类
    if identity == "学生":
        records = get_stu_view_records(ID)  # records 是完整的记录列表, 其中存放Record类
        for record in records:
            tmp = Maintenance_record_for_show(record.report_time, record.reporter_name, record.status, record.id)
            records_for_show.append(tmp)

    elif identity == "管理员":
        records = get_admin_view_records()  # records 是完整的记录列表, 其中存放Record类
        for record in records:
            tmp = Maintenance_record_for_show(record.report_time, record.reporter_name, record.status, record.id)
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

    address = "./static/image/maintenance_pic/" + str(record.id) + ".jpg"
    with open(address, 'wb') as f:
        f.write(record.photo_data)
    address = "/static/image/maintenance_pic/" + str(record.id) + ".jpg"

    if request.method == 'POST':
        print(1)
        finish_record(index)
        return redirect('/maintenance_show')

    return render_template('maintenance_detail.html'
                           , username=username, identity=identity
                           , record=record, address=address)


@app.route('/return_school_apply', methods=['POST', 'GET'])
def return_school_apply():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    ID = session['ID']

    # TODO 未测试
    if request.method == 'POST':
        description = request.form.get('description')
        return_time = request.form.get('return_time')
        apply_for_return(ID, return_time, description)

        return redirect('/student_home')

    return render_template('return_school_apply.html', username=username, identity=identity)


@app.route('/leave_school_apply', methods=['POST', 'GET'])
def leave_school_apply():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    ID = session['ID']

    if request.method == 'POST':
        # example
        departure_time = request.form.get('departure_time')
        return_time = request.form.get('return_time')
        destination = request.form.get('destination')
        description = request.form.get('description')

        apply_for_leave(ID, departure_time, return_time, description, destination)

        return redirect('/student_home')

    return render_template('leave_school_apply.html', username=username, identity=identity)


"""
======================================================== Admin page ===================================================
"""


@app.route('/administrator_home')
def administrator_home():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    return render_template('administrator_home.html', username=username, identity=identity)


@app.route('/IO_school_manage', methods=['POST', 'GET'])
def IO_school_manage():
    if session['state'] is None:
        return redirect('/')

    username = session['username']
    identity = session['identity']
    return render_template('IO_school_manage.html', username=username, identity=identity)


# 用于处理入宿申请
@app.route('/In_school', methods=['POST'])
def In_school():
    id = request.form.get('ID')
    name = request.form.get('name')
    gender = request.form.get('gender')
    birthday = request.form.get('born')
    domicile = request.form.get('domicile')
    classs = request.form.get('class')
    apartment_id = request.form.get('apartment_id')
    room_id = request.form.get('room_id')
    college = request.form.get('college')
    id_card = request.form.get('id_card')
    major = request.form.get('major')
    print(major)

    check_in(id, name, gender, birthday, domicile, classs, apartment_id,
             room_id, college, id_card, major)

    return redirect('/IO_school_manage')


# 用于处理离宿申请
@app.route('/Out_school', methods=['POST'])
def Out_school():
    id = request.form.get('ID_out')

    check_out(id)

    return redirect('/IO_school_manage')


class LR_school_record_for_show:
    def __init__(self, id, room_id, apartment_id, request_id):
        self.content = "申请人ID：" + id + " 公寓号：" + apartment_id + " 房间号：" + room_id
        self.address = request_id


@app.route('/LR_school_manage', methods=['POST', 'GET'])
def LR_school_manage():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    return_requests = get_return_requests()
    leave_requests = get_leave_requests()

    return_requests_for_show = []
    leave_requests_for_show = []

    for request in return_requests:
        return_requests_for_show.append(LR_school_record_for_show(request.student_id, request.room_id,
                                                                  request.apartment_id, request.id))
    for request in leave_requests:
        leave_requests_for_show.append(LR_school_record_for_show(request.student_id, request.room_id,
                                                                 request.apartment_id, request.id))

    return render_template('LR_school_manage.html', username=username, identity=identity,
                           records1=return_requests_for_show, records2=leave_requests_for_show)


# 查看第index个暂离申请，因此需要第index个暂离申请类
# 还要处理上传的修改状态
@app.route('/leave_school_detail/<int:index>', methods=['GET', 'POST'])
def leave_school_detail(index):
    if index < 0:
        return redirect('/LR_school_manage')
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    request = get_single_L_request(index)

    return render_template('leave_school_detail.html', username=username, identity=identity,
                           record=request)


# 用于通过离校申请
@app.route('/agree_leave_school/<int:index>', methods=['POST'])
def agree_leave_school(index):
    update_L_request_status(index, "已通过")

    return redirect('/LR_school_manage')


# 用于不通过离校申请
@app.route('/disagree_leave_school/<int:index>', methods=['POST'])
def disagree_leave_school(index):
    update_L_request_status(index, "不通过")

    return redirect('/LR_school_manage')


# 查看第index个返校申请，因此需要第index个返校申请类
# 还要处理上传的修改状态
@app.route('/return_school_detail/<int:index>', methods=['GET', 'POST'])
def return_school_detail(index):
    if index < 0:
        return redirect('/LR_school_manage')
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    request = get_single_R_request(index)

    return render_template('return_school_detail.html', username=username
                           , identity=identity, record=request)


# 用于通过返校申请
@app.route('/agree_return_school/<int:index>', methods=['POST'])
def agree_return_school(index):
    update_R_request_status(index, "已通过")

    return redirect('/LR_school_manage')


# 用于不通过返校申请
@app.route('/disagree_leave_school/<int:index>', methods=['POST'])
def disagree_return_school(index):
    update_R_request_status(index, "不通过")

    return redirect('/LR_school_manage')


# 需要管理员类（给输入框初始值）
@app.route('/administrator_change', methods=['POST', 'GET'])
def administrator_change():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    ID = session['ID']

    record = get_admin_info(ID)
    user = Admin(record)

    if request.method == 'POST':
        # example
        cell_phone_number = request.form.get('cell_phone_number')
        password = request.form.get('password')
        photo = request.files.get('head')

        if photo.filename != '':
            photo.save("./static/image/admin_head/" + ID + ".jpg")
            with open("./static/image/admin_head/" + ID + ".jpg", 'rb') as f:
                photo_data = f.read()
        # 下为屎山代码 印度大厨
        else:
            # print('photo is none')
            with open("./static/image/admin_head/" + ID + ".jpg", 'wb') as f:
                f.write(user.photo)
            with open("./static/image/admin_head/" + ID + ".jpg", 'rb') as f:
                photo_data = f.read()

        update_admin_info(ID, cell_phone_number, password, photo_data)

        return redirect('/administrator_file')

    return render_template('administrator_change.html', username=username, identity=identity, user=user)


@app.route('/administrator_file')
def administrator_file():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']
    ID = session['ID']

    record = get_admin_info(ID)
    user = Admin(record)

    try:
        with open("./static/image/admin_head/" + ID + ".jpg", 'wb') as f:
            f.write(user.photo)
        address = "/static/image/admin_head/" + ID + ".jpg"
    except Exception:
        address = ""

    return render_template('administrator_file.html', username=username, identity=identity,
                           user=user, address=address)


class Student_record_for_show:
    def __init__(self, id, name, apartment_id, room_id):
        self.content = "ID：" + id + "   姓名：" + name + "    公寓号：" + apartment_id + "    房间号：" + room_id
        self.address = id


@app.route('/student_show', methods=['POST', 'GET'])
def student_show():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    stu_records = get_student_list()
    stu_records_for_show = []

    for student in stu_records:
        tmp = Student_record_for_show(student.id, student.name, student.apartment_id, student.room_id)
        stu_records_for_show.append(tmp)

    return render_template('student_show.html', username=username, identity=identity,
                           records=stu_records_for_show)


@app.route('/admin_change_student/<string:stu_id>', methods=['POST', 'GET'])
def admin_change_student(stu_id):
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    record = get_student_info(stu_id)
    user = Student(record)

    if request.method == 'POST':
        apartment_id = request.form.get('apartment')
        room_id = request.form.get('room')
        new_state = request.form.get('state')

        admin_change_stu(stu_id, apartment_id, room_id, new_state)
        return redirect('/student_show')

    return render_template('admin_change_student.html', username=username, identity=identity,
                           user=user, stu_id=stu_id)


class Guest_record_for_show:
    def __init__(self, id_card, name, arr_time, room_id, dep_time):
        self.content = "姓名：" + name + "   到访时间：" + str(arr_time) + "    房间号：" + room_id + \
                       "    离开时间：" + str(dep_time)
        self.address = id_card


@app.route('/guest_show')
def guest_show():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    guest_records = get_visitor_list()
    guest_records_for_show = []

    for guest in guest_records:
        tmp = Guest_record_for_show(guest.id_card, guest.name, guest.arrive_time, guest.target_room,
                                    guest.departure_time)
        guest_records_for_show.append(tmp)

    return render_template('guest_show.html', username=username, identity=identity,
                           records=guest_records_for_show)


# 查看第index个访客，因此需要第index个访客类
@app.route('/guest_detail/<string:id_card>', methods=['GET', 'POST'])
def guest_detail(id_card):
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    record = get_single_visitor_record(id_card)

    return render_template('guest_detail.html', username=username, identity=identity,
                           id_card=id_card, record=record)


# 处理登记访客
@app.route('/guest_register', methods=['POST', 'GET'])
def guest_register():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    if request.method == 'POST':
        id_card = request.form.get('ID_card')
        name = request.form.get('name')
        identity = request.form.get('category')
        phone = request.form.get('cell_phone_number')
        purpose = request.form.get('purpose')
        target_room = request.form.get('target_room')
        target_apartment = request.form.get('target_apartment')
        departure_time = request.form.get('departure_time')

        register_visitor(id_card, name, identity, phone, purpose, target_room,
                         target_apartment, departure_time)
        return redirect('/guest_show')

    return render_template('guest_register.html', username=username, identity=identity)


# 处理修改访客
@app.route('/guest_change/<string:id_card>', methods=['POST', 'GET'])
def guest_change(id_card):
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    user = get_single_visitor_record(id_card)

    if request.method == 'POST':
        name = request.form.get('name')
        identity = request.form.get('category')
        phone = request.form.get('cell_phone_number')
        purpose = request.form.get('purpose')
        target_room = request.form.get('target_room')
        target_apartment = request.form.get('target_apartment')
        departure_time = request.form.get('departure_time')

        update_visitor(id_card, name, identity, phone, purpose, target_room,
                       target_apartment, departure_time)

        return redirect('/guest_show')

    return render_template('guest_change.html', username=username, identity=identity, id_card=id_card, user=user)


class Room_record_for_show:
    def __init__(self, room_id, president, maintenance_status, stu_num):
        if president == None:
            president = "空"
        self.content = "ID：" + room_id + "   寝室长：" + president + "    维修状态：" + maintenance_status + \
                           "    学生数：" + str(stu_num)
        self.address = room_id


@app.route('/room_show', methods=['POST', 'GET'])
def room_show():
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    room_records = get_room_list()
    room_records_for_show = []

    for room in room_records:
        tmp = Room_record_for_show(room.room_id, room.president, room.maintenance_status,
                                   room.stu_num)
        room_records_for_show.append(tmp)

    return render_template('room_show.html', username=username, identity=identity,
                           records=room_records_for_show)


# 查看第index个宿舍，因此需要第index个宿舍类
@app.route('/room_detail/<string:room_id>', methods=['GET', 'POST'])
def room_detail(room_id):
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    room_record = get_single_room_record(room_id)
    stu_list = get_student_in_room(room_id, room_record.apartment_id)

    return render_template('room_detail.html', username=username
                           , identity=identity, room_id=room_id,
                           room_record=room_record, stu_list=stu_list)


# 处理修改房间
@app.route('/room_change/<string:room_id>', methods=['POST', 'GET'])
def room_change(room_id):
    if session['state'] is None:
        return redirect('/')
    username = session['username']
    identity = session['identity']

    room_record = get_single_room_record(room_id)

    if request.method == 'POST':
        new_president = request.form.get('housemaster')

        update_room_president(room_id, room_record.apartment_id, new_president)

        return redirect('/room_show')

    return render_template('room_change.html', username=username, identity=identity,
                           room_record=room_record, room_id=room_id)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# TODO 学生的返校离校状态变化
#      没有上传照片时查看自身信息会报错
