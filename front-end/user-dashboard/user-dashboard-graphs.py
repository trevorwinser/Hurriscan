import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv('/Users/julie/Documents/310 Project/Infinite-Loopers/data/cleaned_data.csv')

# Assuming the 'date' column is in a suitable format, otherwise parse it as a date
df['date'] = pd.to_datetime(df['date'], format='%y%m%d')

# Plotting zonal winds over time
plt.figure(figsize=(12, 8))
plt.plot(df['date'], df['zon.winds'], label='Zonal Winds')
plt.title('Zonal Winds Over Time')
plt.xlabel('Date')
plt.ylabel('Zonal Winds')
plt.legend()

# Save the zonal winds plot as an image
plt.savefig('/Users/julie/Documents/zonal_winds_plot.png')
plt.close()  # Close the zonal winds plot figure

column_name = 'temp.'

# Binning the data into custom categories
bins = [20, 23, 26, 29, df[column_name].max()]
labels = ['20-22', '23-25', '26-28', '29+']
df['temp_category'] = pd.cut(df[column_name], bins=bins, labels=labels, include_lowest=True)

# Plotting a pie chart based on the custom categories
plt.figure(figsize=(8, 8))
plt.pie(df['temp_category'].value_counts(), labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
plt.title(f'Distribution of {column_name} Categories')

# Save the pie chart as an image
plt.savefig('/Users/julie/Documents/pie_chart.png')
plt.close()  # Close the pie chart figure
