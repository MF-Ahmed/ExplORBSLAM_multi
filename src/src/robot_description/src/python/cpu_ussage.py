import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Initialize lists to store timestamps and average CPU usage percentages
timestamps = []
avg_cpu_percentages = []

# Function to update data
def update_data(frame):
    global timestamps, avg_cpu_percentages
    
    # Get current timestamp
    timestamp = psutil.cpu_times().user + psutil.cpu_times().system
    
    # Append timestamp to list
    timestamps.append(timestamp)
    
    # Get current CPU usage percentage
    cpu_percentage = psutil.cpu_percent(interval=None)
    
    # Append CPU usage percentage to list
    avg_cpu_percentages.append(cpu_percentage)
    
    # Limit data to last 100 entries
    timestamps = timestamps[-3600:]
    avg_cpu_percentages = avg_cpu_percentages[-3600:]
    
    # Clear current plot
    plt.clf()
    
    # Plot average CPU usage percentage
    plt.plot(timestamps, avg_cpu_percentages, label='Average', color='blue', linestyle='-')
    
    # Set plot title and labels
    plt.title('Average CPU Usage Over Time', fontsize=16)
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('CPU Usage (%)', fontsize=14)
    plt.legend(loc='upper right', frameon=False, fontsize=12)
    
    # Set x-axis limits to fix time range
    plt.xlim(left=max(0, timestamp - 3600), right=timestamp)  # Display last 100 seconds
    
    # Add grid lines
    plt.grid(True, linestyle='--', alpha=0.5)
    
# Create animation
ani = animation.FuncAnimation(plt.gcf(), update_data, interval=1000)

# Show plot
plt.show()

