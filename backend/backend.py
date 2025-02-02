from flask import Flask, request, jsonify
import json
import google.generativeai as genai
import PIL.Image


app = Flask(__name__)



# Keep your existing function intact
def get_tag_info(path):
    prompt = """Is this a laundry tag? If so what does each laundry icon on it represent.
    Use this schema:

    {is_tag: bool, tag = {Laundry icon name : Icon instructions}

    For example:

    output could be {True, {"Do not bleach": "This clothing cannot be bleached as it could lead to discoloration."}

    Ensure that each icon's instructions are no more than two sentences.
    """

    genai.configure(api_key="AIzaSyAPfW7HmuKCBDWbNJSd_Ceh9VxbMWVhzYs")  # Gemini API key

    model = genai.GenerativeModel("gemini-1.5-flash")

    user_image = PIL.Image.open(path)

    # Create the prompt with the image data
    response = model.generate_content([prompt, user_image])
    content = response._result.candidates[0].content.parts[0].text

    # Clean the output and parse it into JSON
    content_cleaned = content.strip("```json\n").strip("\n```")
    json_data = json.loads(content_cleaned)
    json_string = json.dumps(json_data)  # json_string is converted to a string

    error_message = {"message": "Image is not a laundry tag"}
    error_msg = json.dumps(error_message)

    if json_data["is_tag"]:
        return json_string
    else:
        return error_msg


@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"message": "No image file provided"}), 400

    image_file = request.files['image']
    # Save the image to a temporary location
    image_path = "temp_image.jpg"
    image_file.save(image_path)

    # Call your function with the saved image path
    result = get_tag_info(image_path)

    # Clean up the temporary image file if necessary
    # os.remove(image_path)  # Uncomment to remove the temporary file

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)