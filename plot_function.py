from matplotlib import pyplot as plt
from table_new.read_excel import excel_to_dataframe

# Main function that selects the shape type and generates the periodic table
def periodic_table():
    df, sheet_name = excel_to_dataframe()

    # Calculate the range of x and y values
    x_range = df['x'].max() - df['x'].min() + 1
    y_range = df['y'].max() - df['y'].min() + 1

    # Scale factor for adjusting the figure size
    scale_factor = 1.5
    figsize_x = x_range * scale_factor
    figsize_y = y_range * scale_factor

    # Create figure and axis with dynamic figsize
    fig, ax = plt.subplots(figsize=(figsize_x, figsize_y))

    # Determine whether to plot rectangles or circles based on the sheet name
    if "table" in sheet_name.lower():
        ax = periodic_table_rectangle(ax, df)
    elif "plot" in sheet_name.lower():
        ax = periodic_table_circle(ax, df)
    else:
        raise ValueError("Sheet name must contain 'table' or 'plot' to specify shape type.")

    # Set axis limits and remove axis ticks/labels and make axes invisible/set aspect ratio to ensure even shapes
    x_margin = 2
    y_margin = 2
    ax.set_xlim(df['x'].min() - x_margin, df['x'].max() + x_margin)
    ax.set_ylim(df['y'].min() - y_margin, df['y'].max() + y_margin)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_aspect('equal')

    return ax

# Function to create a periodic table with rectangles
def periodic_table_rectangle(ax, df):
    for idx, row in df.iterrows():
        include = row['Include']
        if include == 0:
            continue
        
        x = row['x']  # Use the x-coordinate from the DataFrame
        y = row['y']  # Use the y-coordinate from the DataFrame
        symbol = row['Symbol']  # Use the element symbol from the DataFrame

        # Plot the element as a rectangle
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, fill=None, edgecolor='black', lw=2))
        ax.text(x, y, symbol, ha='center', va='center', fontsize=24, weight='bold')
    
    ax.invert_yaxis()
    return ax

# Function to create a periodic table with circles
def periodic_table_circle(ax, df):
    for idx, row in df.iterrows():
        include = row['Include']
        if include == 0:
            continue
        
        x = row['x']  # Use the x-coordinate from the DataFrame
        y = row['y']  # Use the y-coordinate from the DataFrame
        symbol = row['Symbol']  # Use the element symbol from the DataFrame

        # Plot the element as a circle
        ax.add_patch(plt.Circle((x, y), 0.3, fill=None, edgecolor='black', lw=2))
        ax.text(x, y, symbol, ha='center', va='center', fontsize=18)
    
    ax.invert_yaxis()
    return ax