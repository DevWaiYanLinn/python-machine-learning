import numpy as np
import datetime
import pandas as pd
import csv


def main():
    def create_day_range():
        current_date = datetime.date.today()
        fist_day_of_month = current_date.replace(day=1)
        next_month = current_date.replace(day=28) + datetime.timedelta(days=4)
        last_day_of_month = next_month - datetime.timedelta(days=next_month.day)
        date_range = np.arange(fist_day_of_month, last_day_of_month + datetime.timedelta(days=1), dtype='datetime64[D]')
        return np.datetime_as_string(date_range, unit='D')

    def create_field_name():
        return ['Student_ID', *create_day_range(), 'Total', 'Absent']

    def create_csv():
        fields_name = create_field_name()
        df = pd.DataFrame(columns=fields_name)
        df.to_csv('students.csv')

    def create_attendance():
        try:
            df = pd.read_csv('students.csv')
        except FileNotFoundError:
            df = pd.DataFrame()
        student_id = input('Enter Student ID ').strip()
        day_of_month = datetime.date.today().strftime('%Y-%m-%d')
        attendance = input('Enter Attendance: 1 or 0 ')
        new_data = pd.DataFrame({"Student_ID": [student_id], day_of_month: [attendance]})
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv('students.csv', index=False)

    create_attendance()


if __name__ == '__main__':
    main()
