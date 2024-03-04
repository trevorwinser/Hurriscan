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
plt.savefig('user_activity.png')

# Show the plot
plt.show()

