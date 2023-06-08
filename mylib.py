import pymysql

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
        self.romm_id = student_record[6]
        self.college = student_record[7]
        self.id_card = student_record[8]
        self.domicile = student_record[9]
        self.phone = student_record[10]
        self.email = student_record[11]
        self.major = student_record[12]
        self.passward = student_record[13]
        self.state = student_record[14]
        self.photo = student_record[15]

def get_student_info(student_id):
    server = "localhost"  # 服务器名
    user = "root"  # 用户名
    password = "ZSZ1103753519123"  # 密码
    database = "student_apartment"  # 数据库名

    connection = pymysql.connect(host=server,
                                 user=user,
                                 password=password,
                                 database=database)  # 建立连接

    cursor = connection.cursor()  # 创建游标对象
    sql = "SELECT id, name, gender, born, class, apartment_id, room_id, " \
          "college, id_card, domicile, phone, email, major, password, state, photo " \
          f"FROM Student WHERE id = '{student_id}'"
    cursor.execute(sql)
    # print(f"\'{student_id}\'")
    # cursor.callproc('get_student_info', "\'PB20111683\'")
    record = cursor.fetchone()

    connection.close()
    return record