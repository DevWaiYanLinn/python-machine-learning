import numpy as np
import datetime
import pandas as pd
from os import path
import re
import matplotlib.pyplot as plt


def main():
    day_range = []
    month_of_year = datetime.date.today().strftime('%Y-%m')
    file_path = f'{month_of_year}.csv'

    if (not path.isfile(file_path)):
        create_attendance_csv()

    def create_day_range():
        nonlocal day_range
        current_date = datetime.date.today()
        fist_day_of_month = current_date.replace(day=1)
        next_month = current_date.replace(day=28) + datetime.timedelta(days=4)
        last_day_of_month = next_month - \
            datetime.timedelta(days=next_month.day)
        date_range = np.arange(fist_day_of_month, last_day_of_month +
                               datetime.timedelta(days=1), dtype='datetime64[D]')
        day_range = np.datetime_as_string(date_range, unit='D')

    def create_fields_name():
        nonlocal day_range
        return ['Student_ID', *day_range, 'Total', 'Absent']

    def create_attendance_csv():
        month_of_year = datetime.date.today().strftime('%Y-%m')
        fields_name = create_fields_name()
        df = pd.DataFrame(columns=fields_name)
        df.to_csv(f'{month_of_year}.csv', index=False)

    def create_attendance():
        nonlocal month_of_year, file_path
        df = pd.read_csv(file_path)

        student_id = input(
            "Enter student id : id must be maximum 10 character and integer ").strip()

        if not re.match('\d{1,10}', student_id):
            raise TypeError('id must be maximum 10 character and integer')

        attendance = int(input('Enter Attendance: 0 or 1 '))

        if not (attendance == 1 or attendance == 0):
            raise TypeError('attendance must be "0" or "1"')

        day_of_month = datetime.date.today().strftime('%Y-%m-%d')

        format_id = int(student_id.rjust(10, '0'))

        student_record = df["Student_ID"] == format_id

        if (not df.loc[student_record].empty):
            if df.loc[student_record, day_of_month].values[0] != attendance:
                if (attendance):
                    df.loc[student_record, 'Total'] += 1
                    df.loc[student_record, 'Absent'] -= 1
                else:
                    df.loc[student_record, 'Total'] -= 1
                    df.loc[student_record, 'Absent'] += 1
            df.loc[student_record, day_of_month] = attendance
            df.to_csv(file_path, index=False)
        else:
            absent = int(1-attendance)
            attendance = int(attendance)
            new_data = pd.DataFrame(
                {"Student_ID": [format_id], day_of_month: [attendance],
                 'Total': [attendance], 'Absent': [absent]})
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(file_path, index=False)

            print('Attenance record is saved.Do you rollback?')

    def create_chart():
        nonlocal day_range
        month_of_year = datetime.date.today().strftime('%Y-%m')
        file_path = f'{month_of_year}.csv'
        df = pd.read_csv(file_path)
        data = [int(df[x].apply(lambda y: isinstance(y, int) if y else 0).sum())
                for x in day_range]
        plt.pie(data, labels=day_range, autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()

    return [create_attendance, create_chart, create_day_range]


if __name__ == '__main__':
    create_attendance, create_chart, create_day_range = main()
    select_options = int(
        input('Please Choice \n1.For create chart \n2.For create attendance\n'))

    if (select_options == 1):
        create_chart()
    else:
        create_attendance()

    create_day_range()