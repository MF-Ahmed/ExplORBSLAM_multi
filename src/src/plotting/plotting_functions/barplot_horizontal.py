import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Sample data
main_fields = ['Our', 'MAGS', 'Frontier']
sub_fields = ['3R(Synch)', '3R(Asynch)', '2R(Synch)', '2R(Asynch)']
percentages = [
    [60, 52, 49, 45],  # Our     'blue', 'lightblue', 'red', 'pink'
    [0, 50, 0, 45],    # MAGS
    [0, 55, 0, 48]     # Frontier
]

# Define colors for each subfield
colors = ['blue', 'lightblue', 'red', 'pink']

# Set bar height
bar_height = 0.2

# Set Seaborn style
sns.set(style="whitegrid")

# Create figure and axes
fig, ax = plt.subplots(figsize=(6, 3))

# Create bars for each subfield and annotate with percentages
for i, main_field in enumerate(main_fields):
    for j, sub_field in enumerate(sub_fields):
        if percentages[i][j] != 0:
            ax.barh(i + j * bar_height, percentages[i][j], bar_height, label=sub_field, color=colors[j])
            ax.text(percentages[i][j] + 1, i + j * bar_height, f"{percentages[i][j]}%", va='center', fontsize=15)


# Set labels and title
ax.set_ylabel('Method', fontsize=14)
ax.set_xlabel('Map Discovered [%]', fontsize=15)
# Increase font size of x-axis labels
ax.set_xticklabels(ax.get_xticks().astype(int), fontsize=15)
#ax.set_title('Map Discovered by Main and Sub Fields', fontsize=16)
ax.set_yticks(np.arange(len(main_fields)) + bar_height / 2)
ax.set_yticklabels(main_fields, fontsize=15)

# Adjust legend properties
handles, labels = ax.get_legend_handles_labels()
#ax.legend(handles[::-1], labels[::-1], fontsize=14, loc='lower right')

# Remove grid
ax.grid(True)

# Beautify plot
sns.despine()

# Show plot
plt.show()
