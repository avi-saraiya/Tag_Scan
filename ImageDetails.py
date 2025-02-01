import os
from google.generativeai import text
import glob  # For finding multiple tag images

# Set your Gemini API key (replace with your actual key)
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

class ImageDetails:
    def __init__(self):
        self.washing_machine_info = ""
        self.dryer_info = ""
        self.tag_info = {}  # Dictionary to store tag info (key: filename, value: Gemini's response)

    def process_washing_machine(self, image_path):
        self.washing_machine_info = self._get_gemini_info(image_path, "Extract details about this washing machine.")

    def process_dryer(self, image_path):
        self.dryer_info = self._get_gemini_info(image_path, "Extract details about this dryer.")

    def process_tags(self, tag_image_pattern):
        tag_images = glob.glob(tag_image_pattern)  # Find all tag images matching the pattern
        for image_path in tag_images:
            filename = os.path.basename(image_path)  # Use filename as the key
            self.tag_info[filename] = self._get_gemini_info(image_path, "Extract details from this clothing tag.")

    def _get_gemini_info(self, image_path, prompt):  # Helper function to call Gemini
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = image_file.read()

            model = text.Model("gemini-pro-vision")

            response = model.generate_text(
                model=model,
                prompt=prompt,
                image=encoded_image,
            )

            return response.result

        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return f"Error: {e}"  # Return error message

    def __str__(self):  # For easy printing
        output = f"Washing Machine: {self.washing_machine_info}\n"
        output += f"Dryer: {self.dryer_info}\n"
        output += "Tags:\n"
        for filename, info in self.tag_info.items():
            output += f"  {filename}: {info}\n"
        return output


# Example usage:
image_details = ImageDetails()

washing_machine_path = input("Enter path to washing machine image: ")
if os.path.exists(washing_machine_path):
    image_details.process_washing_machine(washing_machine_path)
else:
    print("Washing Machine image not found")

dryer_path = input("Enter path to dryer image: ")
if os.path.exists(dryer_path):
    image_details.process_dryer(dryer_path)
else:
    print("Dryer image not found")


tag_image_pattern = input("Enter pattern for tag image files (e.g., 'tags/*.jpg'): ") # e.g., "tags/*.jpg"
image_details.process_tags(tag_image_pattern)


print(image_details)  # Print all the extracted information

# Access information individually:
# print(image_details.washing_machine_info)
# print(image_details.tag_info["tag1.jpg"]) # Example: Access info for a specific tag image