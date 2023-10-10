            if data['student_id'] == 'All':
                df[data['attendance_date']] = int(data['attend'])
                selected_columns = df.iloc[:, :-2]
                df['total'] = (selected_columns == 1).sum(axis=1)
                df['absent'] = (selected_columns == 0).sum(axis=1)
                df.to_csv('2023-10.csv', index=False)
            else:
                df.set_index('student_id', inplace=True)
                df.loc[data['student_id'], data['attendance_date']] = data['attend']
                present = df.loc[data['student_id']][0:-2] == 1
                absent = df.loc[data['student_id']][0:-2] == 0
                df.loc[data['student_id'], 'total'] = present.sum()
                df.loc[data['student_id'], 'absent'] = absent.sum()
                df.to_csv('2023-10.csv')
