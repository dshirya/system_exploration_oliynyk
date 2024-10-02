import matplotlib.pyplot as plt
from read_excel import excel_to_dataframe  # Importing the function from table.py

# Get the filtered data from table.py
df = excel_to_dataframe()

# Create figure and axis
fig, ax = plt.subplots(figsize=(22, 22))

# Plot each element as a square with bold text using DataFrame values
for idx, row in df.iterrows():
    
    include = row['Include']

    if include == 0:
        continue
    
    x = row['x']  # Use the x-coordinate from the DataFrame
    y = row['y']  # Use the y-coordinate from the DataFrame
    symbol = row['Symbol']  # Use the element symbol from the DataFrame
    
    
    # Plot a square (20x20 points) at the element's position
    ax.add_patch(plt.Circle((x, y), 0.3, fill=None, edgecolor='black', lw=2))
    
    # Add the symbol of the element at the center of the square, bold font
    ax.text(x, y, symbol, ha='center', va='center', fontsize=10, weight='bold')

# Set the aspect ratio to ensure squares are evenly shaped
ax.set_aspect('equal')

# Set axis limits to ensure all elements are visible and create margins
x_margin = 3
y_margin = 1
ax.set_xlim(df['x'].min() - x_margin, df['x'].max() + x_margin)
ax.set_ylim(df['y'].min() - y_margin, df['y'].max() + y_margin)

# Invert the y-axis so that hydrogen is at the top
ax.invert_yaxis()

# Remove axis ticks and labels
ax.set_xticks([])
ax.set_yticks([])

# Make the axes invisible
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Save the plot as a high-quality PNG file
plt.savefig("periodic_table_circles2.png", dpi=300, bbox_inches='tight')

# Show the plot (optional)
#plt.show()