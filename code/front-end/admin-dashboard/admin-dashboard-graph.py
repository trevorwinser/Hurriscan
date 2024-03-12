import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # Importing matplotlib for plotting

# Generate fake user data
days = np.arange(1, 11)  # 10 days
user_counts = np.random.randint(10, 100, size=10)  # Random user counts for each day

# Create a Pandas DataFrame
data = {'Day': days, 'UserCount': user_counts}
df = pd.DataFrame(data)

# Plot the graph using Pandas built-in plotting
df.plot(x='Day', y='UserCount', kind='line', marker='o', linestyle='-')

# Add title and labels
plt.title('User Activity Over 10 Days')
plt.xlabel('Day')
plt.ylabel('Number of Users')

# Save the plot
plt.savefig('/Users/julie/Documents/user_activity.png')

# Show the plot
plt.show()

# Generate fake step data for different days
days = pd.date_range(start='2024-01-01', end='2024-01-10')  # 10 days
steps = np.random.randint(1000, 10000, size=len(days))  # Random steps taken each day

# Create a Pandas DataFrame
data = {'Date': days, 'Steps': steps}
df = pd.DataFrame(data)

# Plot the line graph using Pandas built-in plotting
df.plot(x='Date', y='Steps', marker='o', linestyle='-')

# Add title and labels
plt.title('Daily Steps Taken')
plt.xlabel('Date')
plt.ylabel('Steps')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Save the plot
plt.savefig('/Users/julie/Documents/steps_taken.png')

# Show the plot
plt.show()
