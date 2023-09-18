import csv
import matplotlib.pyplot as plt
with open('student.csv', 'r') as student_csv:
    read_student_csv = csv.DictReader(student_csv)
    colors = ['cyan', 'green', 'orange', 'red']

    bmi_data = {
        'Normal': 0,
        'Underweight': 0,
        'Overweight': 0,
        'Obese': 0,
    }
    for student in read_student_csv:
        bmi = float(student['weight']) / ((float(student['height'])/ 3.281) * 2)

        if bmi < 18:
            bmi_data['Normal'] += 1
        elif bmi >= 18 and bmi <= 22.9:
            bmi_data['Underweight'] += 1
        elif bmi >= 23.0 and bmi <= 24.9:
            bmi_data['Overweight'] += 1
        else:
            bmi_data['Obese'] += 1

    print(bmi_data.values())
    labels = bmi_data.keys()
    sizes = bmi_data.values()

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title('BMI of Students')
    plt.axis('equal') 
    plt.show()
