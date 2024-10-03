import matplotlib.pyplot as plt
from read_excel import excel_to_dataframe  # Importing the function from table.py

# Get the filtered data and sheet name from table.py
df, sheet_name = excel_to_dataframe()

# Calculate the range of x and y values
x_range = df['x'].max() - df['x'].min() + 1  # Adding 1 to ensure the full range is covered
y_range = df['y'].max() - df['y'].min() + 1

# Scale factor for adjusting the figure size (adjust as needed based on the visual output)
scale_factor = 1.5

# Set figure size dynamically based on x and y ranges
figsize_x = x_range * scale_factor
figsize_y = y_range * scale_factor

# Create figure and axis with dynamic figsize
fig, ax = plt.subplots(figsize=(figsize_x, figsize_y))

# Determine whether to plot rectangles or circles based on the sheet name
if "table" in sheet_name.lower():
    shape_type = 'rectangle'
elif "plot" in sheet_name.lower():
    shape_type = 'circle'
else:
    raise ValueError("Sheet name must contain 'table' or 'plot' to specify shape type.")

# Plot each element with the chosen shape type
for idx, row in df.iterrows():
    
    include = row['Include']

    if include == 0:
        continue
    
    x = row['x']  # Use the x-coordinate from the DataFrame
    y = row['y']  # Use the y-coordinate from the DataFrame
    symbol = row['Symbol']  # Use the element symbol from the DataFrame
    
    if shape_type == 'rectangle':
        ax.add_patch(plt.Rectangle((x-0.5, y-0.5), 1, 1, fill=None, edgecolor='black', lw=2))
        ax.text(x, y, symbol, ha='center', va='center', fontsize=24, weight='bold')
        ax.invert_yaxis()
    elif shape_type == 'circle':
        ax.add_patch(plt.Circle((x, y), 0.3, fill=None, edgecolor='black', lw=2))
        ax.text(x, y, symbol, ha='center', va='center', fontsize=18)
    

# Set the aspect ratio to ensure squares or circles are evenly shaped
ax.set_aspect('equal')

# Set axis limits to ensure all elements are visible and create margins
x_margin = 2
y_margin = 2
ax.set_xlim(df['x'].min() - x_margin, df['x'].max() + x_margin)
ax.set_ylim(df['y'].min() - y_margin, df['y'].max() + y_margin)

# Remove axis ticks and labels and make the axes invisible
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Save the plot as a high-quality PNG file
if shape_type == 'rectangle':
    plt.savefig("periodic_table.png", dpi=300, bbox_inches='tight')
elif shape_type == 'circle':
    plt.savefig("periodic_circles.png", dpi=300, bbox_inches='tight')

# Show the plot (optional)
#plt.show()