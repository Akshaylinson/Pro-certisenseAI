from PIL import Image, ImageDraw, ImageFont

# Create a 64x64 icon (will be scaled for favicon)
size = 64
img = Image.new('RGB', (size, size), color='white')
draw = ImageDraw.Draw(img)

# Draw a shield shape
shield_points = [
    (32, 8),   # Top center
    (52, 14),  # Top right
    (50, 38),  # Middle right
    (32, 56),  # Bottom center
    (14, 38),  # Middle left
    (12, 14)   # Top left
]

# Scale points to fit in 64x64
scale = 0.9
offset = 4
scaled_points = [
    ((x - 32) * scale + 32, (y - 8) * scale + offset) 
    for x, y in shield_points
]

# Draw shield outline
draw.polygon(scaled_points, fill='#2563eb', outline='#1e40af', width=2)

# Add a checkmark inside the shield
check_x = [24, 30, 42]
check_y = [34, 42, 24]
draw.line([(check_x[0], check_y[0]), (check_x[1], check_y[1])], fill='white', width=4)
draw.line([(check_x[1], check_y[1]), (check_x[2], check_y[2])], fill='white', width=4)

# Save as PNG
img.save('favicon.png', 'PNG')
print("Favicon created successfully!")
