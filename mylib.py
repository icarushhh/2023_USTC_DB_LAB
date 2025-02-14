import pymysql
from datetime import datetime

"""
============================================ Connect to database ========================================
"""
server = "localhost"  # 服务器名
user = "root"  # 用户名
password = ""  # 密码
database = "student_apartment"  # 数据库名

connection = pymysql.connect(host=server,
                             user=user,
                             password=password,
                             database=database)  # 建立连接

cursor = connection.cursor()  # 创建游标对象

"""
=================================================== Student =============================================
"""


class Student(object):
    """
    Store the info of a student
    """

    def __init__(self, student_record):
        self.id = student_record[0]
        self.name = student_record[1]
        self.gender = student_record[2]
        self.birth = student_record[3]
        self.classs = student_record[4]
        self.apartment_id = student_record[5]
        self.room_id = student_record[6]
        self.college = student_record[7]
        self.id_card = student_record[8]
        self.domicile = student_record[9]
        self.phone = student_record[10]
        self.email = student_record[11]
        self.major = student_record[12]
        self.password = student_record[13]
        self.state = student_record[14]
        self.photo = student_record[15]


def get_student_info(student_id):
    """
    :param student_id:
    :return: record of the student
    """

    # sql = "SELECT id, name, gender, born, class, apartment_id, room_id, " \
    #       "college, id_card, domicile, phone, email, major, password, state, photo " \
    #       f"FROM Student WHERE id = '{student_id}'"
    # cursor.execute(sql)
    args = (student_id,)
    cursor.callproc('get_student_info', args)
    record = cursor.fetchone()
    return record


def update_student_info(id, phone, email, password, photo):
    """
    in page student_change, update student info
    """
    args = (id, photo, phone, email, password)
    cursor.callproc('update_student_info', args)
    connection.commit()

    return


def report_maintenance(student_id, description, photo):
    """
    report a maintenance
    """
    record = get_student_info(student_id)
    reporter = Student(record)

    args = (student_id, reporter.room_id, reporter.apartment_id, description, photo)
    cursor.callproc('report_maintenance', args)
    connection.commit()

    return


def apply_for_return(student_id, return_time, description):
    args = (student_id, return_time, description)
    cursor.callproc('apply_for_return', args)
    connection.commit()

    return


def apply_for_leave(student_id, leave_time, expected_return_time, purpose, destination):
    args = (student_id, leave_time, expected_return_time, purpose, destination)
    cursor.callproc('apply_for_leave', args)
    connection.commit()

    return


"""
================================================= Administrator =====================================================
"""


class Admin(object):
    """
    Store the info of a administrator
    """

    def __init__(self, admin_record):
        self.id = admin_record[0]
        self.gender = admin_record[1]
        self.name = admin_record[2]
        self.id_card = admin_record[3]
        self.phone = admin_record[4]
        self.apartment_id = admin_record[5]
        self.schedule = admin_record[6]
        self.password = admin_record[7]
        self.photo = admin_record[8]


def get_admin_info(admin_id):
    """
    :param admin_id:
    :return: a record of administrator
    """

    sql = "SELECT id, gender, name, id_card, phone, apartment_id, " \
          "schedule, password, photo " \
          f"FROM Manager WHERE id = '{admin_id}';"
    cursor.execute(sql)
    record = cursor.fetchone()

    return record


def update_admin_info(id, phone, password, photo):
    """
    update admin info
    """
    args = (id, phone, password, photo)
    cursor.callproc('update_manager_info', args)
    connection.commit()

    return


def check_in(id, name, gender, birthday, domicile, classs, apartment_id,
             room_id, college, id_card, major):
    """
    check in a student
    """
    args = (id, name, gender, str(birthday), classs, college, id_card, domicile,
            "未设置", "未设置", major, room_id, apartment_id)
    cursor.callproc('check_in', args)
    connection.commit()

    return


def check_out(id):
    """
    check out a student
    """
    args = (id,)
    cursor.callproc("check_out", args)
    connection.commit()

    return


def get_return_requests():
    """
    get all the return_school records from database,
    return a list of Return_request class
    """

    sql = "SELECT * from ReturnApplication"
    cursor.execute(sql)
    records = cursor.fetchall()

    requests = []
    for record in records:
        tmp = Return_request(record)
        requests.append(tmp)

    return requests


def get_leave_requests():
    """
    get all the leave_school records from database,
    return a list of Leave_request class
    """

    sql = "SELECT * from LeaveApplication"
    cursor.execute(sql)
    records = cursor.fetchall()

    requests = []
    for record in records:
        tmp = Leave_request(record)
        requests.append(tmp)

    return requests


def update_L_request_status(request_id, new_status):
    """
    update the approval_status of a leave request to new status
    """
    args = (request_id, new_status)
    cursor.callproc("update_leave_status", args)
    connection.commit()

    return


def update_R_request_status(request_id, new_status):
    """
    update the approval_status of a return request to new status
    """
    args = (request_id, new_status)
    cursor.callproc("update_return_status", args)
    connection.commit()

    return


def get_student_list():
    """
    get all the student records from database,
    return a list of Student class
    """
    sql = "SELECT * from Student"
    cursor.execute(sql)
    records = cursor.fetchall()

    return_list = []
    for record in records:
        tmp = Student(record)
        return_list.append(tmp)

    return return_list


def admin_change_stu(stu_id, apartment_id, room_id, new_state):
    """
    admin change student info
    """
    args = (stu_id, apartment_id, room_id)
    cursor.callproc("update_student_room", args)
    connection.commit()

    args = (stu_id, new_state)
    cursor.callproc("update_student_state", args)
    connection.commit()

    return


def get_visitor_list():
    """
    get all the visitor records from database,
    return a list of Visitor class
    """
    sql = "SELECT * from Visitor"
    cursor.execute(sql)
    records = cursor.fetchall()

    return_list = []
    for record in records:
        tmp = Visitor(record)
        return_list.append(tmp)

    return return_list


def register_visitor(id_card, name, identity, phone, purpose, target_room,
                     target_apartment, departure_time):
    """
    register a visitor
    """
    args = (id_card, name, identity, phone, purpose, target_room,
            target_apartment, departure_time)
    cursor.callproc("register_visitor", args)
    connection.commit()

    return


def update_visitor(id_card, name, identity, phone, purpose, target_room,
                   target_apartment, departure_time):
    """
    update the info of a visitor
    """
    args = (id_card, name, identity, phone, purpose, target_room,
            target_apartment, departure_time)
    cursor.callproc("update_visitor", args)
    connection.commit()

    return


def get_room_list():
    """
    get all the room records from database,
    return a list of Room class
    """
    sql = "SELECT * from Room"
    cursor.execute(sql)
    records = cursor.fetchall()

    return_list = []
    for record in records:
        tmp = Room(record)
        return_list.append(tmp)

    return return_list


def update_room_president(room_id, apartment_id, new_president):
    """
    update the president of a room
    """
    args = (room_id, apartment_id, new_president)
    cursor.callproc("update_room_president", args)
    connection.commit()

    return


"""
======================================================== Maintenance_record ===========================================
"""


class Maintenance_record(object):
    """
    Store the info of a maintenance record
    """

    def __init__(self, maintenance_record):
        self.id = maintenance_record[0]
        self.room_id = maintenance_record[1]
        self.apartment_id = maintenance_record[2]
        self.reporter_id = maintenance_record[3]
        self.fault_info = maintenance_record[4]
        self.status = maintenance_record[5]
        self.person_in_charge = maintenance_record[6]
        self.report_time = maintenance_record[7]
        self.finish_time = maintenance_record[8]

        self.photo_data = maintenance_record[9]
        self.reporter_name = maintenance_record[10]


def get_single_record(record_id):
    """
    get the maintenance record with given id, return a Record class
    """

    sql = f"select * from Maintenance where id = '{record_id}';"
    cursor.execute(sql)
    record_without_name = cursor.fetchone()

    sql = "select photo from MaintenancePhotos " \
          f"where maintenance_id = '{record_id}';"
    cursor.execute(sql)
    photo_data = cursor.fetchone()[0]

    sql = "select name from Student " \
          "where Student.id = " \
          f"(select reporter_id from Maintenance where Maintenance.id = '{record_id}'); "
    cursor.execute(sql)
    name = cursor.fetchone()[0]

    record = []
    for x in record_without_name:
        record.append(x)
    record.append(photo_data)
    record.append(name)

    result = Maintenance_record(record)

    return result


def finish_record(record_id):
    """
    change the status of a record to Finished
    """

    args = (record_id, "已完成")
    cursor.callproc('update_maintenance_status', args)
    connection.commit()

    return


def get_stu_view_records(student_id):
    """
    student view of maintenance records, return a list of Record class
    """

    args = (student_id,)
    cursor.callproc('get_apartment_maintenance_student', args)
    records = cursor.fetchall()

    result = []

    for record in records:
        tmp = Maintenance_record(record)
        result.append(tmp)

    return result


def get_admin_view_records():
    """
    administrator view of maintenance records, return a list of Record class
    """

    args = ()
    cursor.callproc('get_apartment_maintenance_administrator', args)
    records = cursor.fetchall()

    result = []

    for record in records:
        tmp = Maintenance_record(record)
        result.append(tmp)

    return result


"""
======================================================== LR_school_request ===========================================
"""


# 离校申请类
class Leave_request(object):
    """
    Store the info of a leave_school request
    """

    def __init__(self, leave_school_record):
        self.id = leave_school_record[0]
        self.student_id = leave_school_record[1]
        self.room_id = leave_school_record[2]
        self.apartment_id = leave_school_record[3]
        self.leave_time = leave_school_record[4]
        self.expected_return_time = leave_school_record[5]
        self.purpose = leave_school_record[6]
        self.destination = leave_school_record[7]
        self.approval_status = leave_school_record[8]


# 返校申请类
class Return_request(object):
    """
    Store the info of a return_school record
    """

    def __init__(self, return_school_record):
        self.id = return_school_record[0]
        self.student_id = return_school_record[1]
        self.room_id = return_school_record[2]
        self.apartment_id = return_school_record[3]
        self.return_time = return_school_record[4]
        self.purpose = return_school_record[5]
        self.approval_status = return_school_record[6]



def get_single_R_request(return_request_id):
    """
    get single return school request
    """
    sql = f"select * from ReturnApplication where id = '{return_request_id}';"
    cursor.execute(sql)
    record = cursor.fetchone()
    request = Return_request(record)

    return request


def get_single_L_request(leave_request_id):
    """
    get single leave school request
    """
    sql = f"select * from LeaveApplication where id = '{leave_request_id}';"
    cursor.execute(sql)
    record = cursor.fetchone()
    request = Leave_request(record)

    return request


"""
======================================================== Visitor class =================================================
"""


class Visitor(object):
    """
    Store the info of a visitor record
    """

    def __init__(self, visitor_record):
        self.id_card = visitor_record[0]
        self.name = visitor_record[1]
        self.identity = visitor_record[2]
        self.phone = visitor_record[3]
        self.purpose = visitor_record[4]
        self.target_room = visitor_record[5]
        self.target_apartment = visitor_record[6]
        self.arrive_time = visitor_record[7]
        self.departure_time = visitor_record[8]


def get_single_visitor_record(id_card):
    """
    get single visitor record
    return a Visitor class
    """
    sql = f"select * from Visitor where id_card = '{id_card}';"
    cursor.execute(sql)
    record = cursor.fetchone()
    visitor = Visitor(record)

    return visitor


"""
======================================================== Room class =================================================
"""


class Room(object):
    """
    Store the info of a room
    """

    def __init__(self, record):
        self.room_id = record[0]
        self.apartment_id = record[1]
        self.capacity = record[2]
        self.stu_num = record[3]
        self.president = record[4]
        self.maintenance_status = record[5]


def get_single_room_record(room_id):
    """
    get single room record
    return a Room class
    """
    sql = f"select * from Room where id = '{room_id}';"
    cursor.execute(sql)
    record = cursor.fetchone()
    room = Room(record)

    return room


def get_student_in_room(room_id, apartment_id):
    """
    get stu live in the room
    return a list of stu name
    """
    args = (room_id, apartment_id)
    cursor.callproc('GetStudentsInRoom', args)
    names_tuple = cursor.fetchall()
    stu_names = []
    for name in names_tuple:
        stu_names.append(name[0])
    for i in range(4-len(names_tuple)):
        stu_names.append("无")

    return stu_names






