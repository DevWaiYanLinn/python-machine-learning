import pandas as pd
import matplotlib.pyplot as plt

# Create a DataFrame from the CSV-like data
df = pd.read_csv('data.csv')

# Convert the 'Date' column to a datetime object
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')

# Group by month and calculate the average prices
monthly_data = df.groupby(df['Date'].dt.to_period('M')).mean()

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(monthly_data.index.to_timestamp(), monthly_data['Open'], marker='o', linestyle='-', label='Open', color='red')
plt.plot(monthly_data.index.to_timestamp(), monthly_data['High'], marker='o', linestyle='-', label='High', color='green')
plt.plot(monthly_data.index.to_timestamp(), monthly_data['Low'], marker='o', linestyle='-', label='Low', color='blue')
plt.plot(monthly_data.index.to_timestamp(), monthly_data['Close'], marker='o', linestyle='-', label='Close', color='purple')
plt.title('Average Monthly Prices')
plt.xlabel('Month')
plt.ylabel('Price')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
