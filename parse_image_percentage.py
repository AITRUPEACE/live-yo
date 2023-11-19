from PIL import Image
import numpy as np

# Load the image
image_path = './elementScreenshot_75_2.png'
image = Image.open(image_path)

# Convert image to numpy array
image_np = np.array(image)

# Define the color for the orange and grey bars
# Colors are in RGB format
orange_bar_color = np.array([242, 139, 130]) # RGB for #f28b82
grey_bar_color = np.array([95, 99, 104]) # RGB for #5f6368

# Function to calculate the percentage of the orange bar against the grey bar
def calculate_percentage(image_np, orange_bar_color, grey_bar_color):
    # Find the pixels that match the orange and grey bar colors
    orange_pixels = np.all(image_np[:, :, :3] == orange_bar_color, axis=-1)
    grey_pixels = np.all(image_np[:, :, :3] == grey_bar_color, axis=-1)

    # Sum the pixels for each bar
    orange_bar_length = np.sum(orange_pixels)
    #print(f"orange bar length: {orange_bar_length}px")
    grey_bar_length = np.sum(grey_pixels)
    #print(f"grey bar length: {grey_bar_length}px")

    # Calculate the percentage of the orange bar against the grey bar
    if grey_bar_length > 0:
        percentage = (orange_bar_length / grey_bar_length) * 100
    else:
        percentage = 0  # Prevent division by zero

    return percentage

# Calculate the percentage
percentage = round(calculate_percentage(image_np, orange_bar_color, grey_bar_color))
print(percentage)
if percentage > 100: # Prevent percentage from exceeding 100%
    percentage = 100
print(f"The location {percentage}% of usual")
