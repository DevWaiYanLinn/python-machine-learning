import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv', date_format='%m/%d/%y', parse_dates=['Date'])
df = df.sort_values(by='Date')

# Determine the number of columns in the DataFrame (excluding the 'Date' column)
num_columns = len(df.columns) - 1

# Create subplots
fig, axes = plt.subplots(1, num_columns, figsize=(15, 5))

colors = ['red', 'green', 'blue', 'orange']

# Loop through each column (excluding 'Date') and create a subplot
for i, key in enumerate(df.columns[1:]):
    axes[i].plot(df['Date'], df[key], label=f'{key}', marker='.', color=colors[i])
    axes[i].tick_params(axis='x', rotation=45)
    axes[i].set_title(f'{key}')
    axes[i].set_xlabel('Date')
    axes[i].set_ylabel('Price')
    axes[i].grid(True)
    axes[i].legend()

# Set a common title and adjust layout
fig.suptitle('Stock Price Chart (Open, High, Low, Close)', fontsize=16)
plt.tight_layout()

# Show the chart
plt.show()
