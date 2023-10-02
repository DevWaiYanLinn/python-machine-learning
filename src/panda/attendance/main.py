import numpy as np
import datetime
import pandas as pd
from os import path
import re


def main():
    day_range = []
    month_of_year = datetime.date.today().strftime('%Y-%m')
    file_path = f'{month_of_year}.csv'
    colors = {'error': '\033[91m', "end": '\033[0m', 'warning': '\033[93m'}
    day_of_month = datetime.date.today().strftime('%Y-%m-%d')

    def create_day_range():
        nonlocal day_range
        current_date = datetime.date.today()
        fist_day_of_month = current_date.replace(day=1)
        next_month = current_date.replace(day=28) + datetime.timedelta(days=4)
        last_day_of_month = next_month - datetime.timedelta(days=next_month.day)
        date_range = np.arange(fist_day_of_month, last_day_of_month +
                               datetime.timedelta(days=1), dtype='datetime64[D]')
        day_range = np.datetime_as_string(date_range, unit='D')

    def create_fields_name():
        return ['student_id', 'name', *day_range, 'total', 'absent']

    def create_attendance_csv():
        fields_name = create_fields_name()
        df = pd.DataFrame(columns=fields_name)
        df.to_csv(f'{month_of_year}.csv', index=False)

    def get_student_id():
        while True:
            print("Enter student id : id must be maximum 10 character and integer")
            student_id = input().strip()
            if not re.match(r"\d{1,10}", student_id):
                print(f'{colors["error"]}id must be maximum 10 character and integer{colors["end"]}')
            else:
                return "AI-1-" + f"{student_id}".rjust(5, '0')

    def get_student_attendance():
        while True:
            print('Enter Attendance')
            print('1.yes')
            print('0.no')
            attendance = input()
            if not re.match(r"[0-1]", attendance):
                print(f'{colors["error"]}Attendance must be "0" or "1"{colors["end"]}')
            else:
                return int(attendance)

    def get_student_name():
        while True:
            print('Enter Student name')
            name = input()
            if not re.match(r"[A-Za-z\s]", name):
                print(f'{colors["error"]}Name must be only word character{colors["end"]}')
            else:
                return name

    def create_attendance():
        student_id = get_student_id()
        attendance_date = day_of_month
        df = pd.read_csv(file_path)
        attended_record = df["student_id"] == student_id
        if not df.loc[attended_record, attendance_date].empty:
            print(
                f'{colors["warning"]}The attendance for student id({student_id}) is already recorded for today.')
            print(f'Do you want to update?{colors["end"]}')
            print('1.yes')
            print('0.no')
            is_update = input()
            if is_update == '0':
                return print('Finished')

        if not df.loc[attended_record].empty:
            student_attendance = get_student_attendance()
            if df.loc[attended_record, attendance_date].values[0] != student_attendance:
                if student_attendance:
                    df.loc[attended_record, 'total'] += 1
                    df.loc[attended_record, 'absent'] -= 1
                else:
                    df.loc[attended_record, 'total'] -= 1
                    df.loc[attended_record, 'absent'] += 1
            df.loc[attended_record, attendance_date] = student_attendance
        else:
            student_name = get_student_name()
            student_attendance = get_student_attendance()
            absent = int(1 - student_attendance)
            student_attendance = int(student_attendance)
            new_data = pd.DataFrame(
                {"student_id": [student_id], "name": [student_name], attendance_date: [student_attendance],
                 'total': [student_attendance], 'absent': [absent]})
            df = pd.concat([df, new_data], ignore_index=True)

        df.to_csv(file_path, index=False)
        print('Attendance record is saved')

    def start():
        create_day_range()
        if not path.isfile(file_path):
            create_attendance_csv()
        create_attendance()

    start()


if __name__ == '__main__':
    main()
