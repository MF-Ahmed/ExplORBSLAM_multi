import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Define the directory where your .npy files are located
data1_directory = '/home/usr/data/ExplOrbSLAM_working/src/src/plotting/data'  # Our
data2_directory = '/home/usr/data/ExplOrbSLAM_working/src/src/plotting/data'  # Our
data3_directory = '/home/usr/data/ExplOrbSLAM_working/src/src/plotting/data'  # Our

def proc_data_for_plotting(data_directory):
    # Initialize lists to store data from all files
    all_data = []

    start_x = 0  # Set this based on your data
    end_x = 1200  # Set this based on your data

    # Define the number of points for interpolation
    num_points = 250  # Adjust based on the level of detail you need

    # Create a common set of x-values (assuming you know the range)
    common_x = np.linspace(start_x, end_x, num_points)

    # Loop through .npy files in the directory
    for filename in os.listdir(data_directory):
        if filename.endswith('.npy'):
            file_path = os.path.join(data_directory, filename)
            # Load data from the .npy file
            # data = np.load(file_path)
            data = np.load(os.path.join(data_directory, filename), allow_pickle=True).item()

            # Find the minimum and maximum values in 'merged_x'
            min_value = min(data['merged_x'])
            max_value = max(data['merged_x'])

            # Normalize 'merged_x' to be between 0 and 1200
            data['merged_x'] = [(x - min_value) / (max_value - min_value) * 1500 for x in data['merged_x']]

            # Interpolate data to the common x-values
            x = data['merged_x']  # Assuming x values are in the first column
            y = (data['merged_y'] / data['generated_map_area']) * 100   # Assuming y values are in the second column
            interpolated_y = np.interp(common_x, x, y)

            # Append the interpolated data to the list
            all_data.append(interpolated_y)

    # Check if any data was loaded
    if not all_data:
        print("No data found in the specified directory.")
    else:
        # Calculate the average and standard deviation across all files
        all_data = np.vstack(all_data)  # Stack all data into one array
        average = np.mean(all_data, axis=0)
        std_deviation = np.std(all_data, axis=0)
        # Find the x-value corresponding to the maximum y-value
        max_index = np.argmax(average)
        max_x = common_x[max_index]
        max_y = average[max_index]

    return max_index, max_x, max_y, common_x, average, std_deviation


# Create a beautiful line plot
plt.figure(figsize=(6, 3))

for i, data_directory in enumerate([data1_directory, data2_directory, data3_directory]):
    label = ''
    color = ''
    if i == 0:
        label = "3R_Our (Asynch)"
        color = 'royalblue'
    elif i == 1:
        label = "3R_MAGS"
        color = 'red'
    elif i == 2:
        label = "3R_Frontier"
        color = 'green'

    max_index, max_x, max_y, common_x, average, std_deviation = proc_data_for_plotting(data_directory)
    plt.plot(common_x, average, label=label, color=color, linewidth=2)
    plt.fill_between(common_x, average - std_deviation, average + std_deviation, alpha=0.2, color=color)

    # Mark the maximum value with a red dot and annotate it
    plt.plot(max_x, max_y, marker='o', markersize=8, color=color, linestyle='None')
    plt.annotate(f"Max ({max_y:.2f})", (max_x, max_y), textcoords="offset points", xytext=(0, 10), ha='center')

plt.xlabel("Time [s]", fontsize=14)
plt.ylabel("Map discovered [%]", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=10)
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
