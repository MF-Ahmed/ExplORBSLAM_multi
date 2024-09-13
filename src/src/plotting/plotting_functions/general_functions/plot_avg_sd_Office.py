import numpy as np
import matplotlib.pyplot as plt
import os

# Specify the directory where your .npy files are located
data1_directory = 'F:\\My Papers\\single_robot\\Results\\results\\results_realrobot\\npy\\util'
data2_directory = 'F:\\My Papers\\single_robot\\Results\\results\\results_realrobot\\npy\\noutil'

# Get a list of .npy files in the directory

def plot_data(data_directory):

    npy_files = [f for f in os.listdir(data_directory) if f.endswith('.npy')]

    # Initialize lists to store data
    x_values_list = []
    y_values_list = []

    # Loop through each .npy file
    for npy_file in npy_files:
        # Load data from the .npy file
        data = np.load(os.path.join(data_directory, npy_file), allow_pickle=True).item()
        
        # Assuming data has two columns: x and y
        x_data = data['merged_x']
        y_data = data['merged_y']/data['generated_map_area']*100
        
        # Append x and y data to the respective lists
        x_values_list.append(x_data)
        y_values_list.append(y_data)

    # Find a common set of x values for interpolation
    common_x_values = np.unique(np.concatenate(x_values_list))

    # Interpolate or resample the y data to the common x values
    interpolated_y_values_list = [np.interp(common_x_values, x, y) for x, y in zip(x_values_list, y_values_list)]

    # Calculate the mean and standard deviation for the interpolated y data
    mean_y_values = np.mean(interpolated_y_values_list, axis=0)
    std_dev_y_values = np.std(interpolated_y_values_list, axis=0)

    return common_x_values,mean_y_values



plt.figure(figsize=(10, 6))

common_x_values,mean_y_values = plot_data(data1_directory)

# Create a line plot for the mean y values

plt.plot(common_x_values/max(common_x_values), mean_y_values, label='Our', color='r')

common_x_values,mean_y_values = plot_data(data2_directory)

# Create a line plot for the mean y values
plt.plot(common_x_values/max(common_x_values), mean_y_values, label='AGS', color='b')

# Plot the shaded error region for standard deviation
#plt.fill_between(common_x_values, mean_y_values - std_dev_y_values, mean_y_values + std_dev_y_values, color='lightgray', alpha=0.7, label='Std Dev Y')




plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Line Plot of Mean Y with Standard Deviation')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
