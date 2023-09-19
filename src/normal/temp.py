import csv
import matplotlib.pyplot as plt

with open('data.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = {}
    for csv_data in csv_reader:
        month = csv_data['Date'].split('/')[0]
        if month not in data:
            data[month] = {
                'Open': [],
                'High': [],
                'Low': [],
                'Close': []
            }
        else:
            data[month]['Open'].append(float(csv_data['Open'].strip()))
            data[month]['High'].append(float(csv_data['High'].strip()))
            data[month]['Low'].append(float(csv_data['Low'].strip()))
            data[month]['Close'].append(float(csv_data['Close'].strip()))

    months = data.keys()
    for month in months:
        data[month]['Open'] = sum(data[month]['Open']) / len(data[month]['Open'])
        data[month]['High'] = sum(data[month]['High']) / len(data[month]['High'])
        data[month]['Close'] = sum(data[month]['Close']) / len(data[month]['Close'])
        data[month]['low'] = sum(data[month]['Low']) / len(data[month]['Low'])
