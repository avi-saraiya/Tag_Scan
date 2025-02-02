import os
# This program only puts out a message upon receiving the uploaded image. This simulates the paragrpah that Gemini will return
def process_image(image_path):
    if not os.path.exists(image_path):
        return "Error: Image file not found."
    
    return "Image detected successfully."