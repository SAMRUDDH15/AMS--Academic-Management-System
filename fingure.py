from PIL import Image, ImageDraw

# Image size and background color
width, height = 100, 100
background_color = (255, 255, 255)  # White

# Create a new image with a white background
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

# Define the finger color and coordinates
finger_color = (255, 0, 0)  # Red
finger_coordinates = [(50, 10), (50, 70)]  # Line from (50, 10) to (50, 70)

# Draw the finger
draw.line(finger_coordinates, fill=finger_color, width=10)

# Save the icon
image.save("index_finger_icon.png")

# Show the icon
image.show()
