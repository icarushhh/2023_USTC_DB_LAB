import pymysql

# connect to database
server = "localhost"  # 服务器名
user = "root"  # 用户名
password = ""  # 密码
database = "student_apartment"  # 数据库名

connection = pymysql.connect(host=server,
                             user=user,
                             password=password,
                             database=database)  # 建立连接

cursor = connection.cursor()  # 创建游标对象


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
    args = (student_id, )
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


class Admin(object):
    """
    Store the info of a administrator
    """

    def __init__(self, student_record):
        self.id = student_record[0]
        self.gender = student_record[1]
        self.name = student_record[2]
        self.id_card = student_record[3]
        self.phone = student_record[4]
        self.apartment_id = student_record[5]
        self.schedule = student_record[6]
        self.password = student_record[7]
        self.photo = student_record[8]


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
