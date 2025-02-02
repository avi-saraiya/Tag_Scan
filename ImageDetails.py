from fastapi import FastAPI, File, UploadFile
from typing import Optional
import PIL.Image
import google.generativeai as genai

app = FastAPI()

# Store responses for washing machine, dryer, and clothing tag instructions
washing_machine_info: Optional[str] = None
dryer_info: Optional[str] = None
clothing_tag_instructions = []

# Configure the Gemini API
genai.configure(api_key="GEMINI_API_KEY")

def call_gemini_api(image: UploadFile, prompt: str) -> str:
    """ Sends the image to Gemini API and retrieves the response """
    # Open image using PIL
    image_file = PIL.Image.open(image.file)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel(model_name="gemini-1.5.pro")
    
    # Get response from the Gemini API
    response = model.generate_content(prompt, image_file)
    
    # Return the result as text
    return response.text

@app.post("/upload/washing-machine")
def upload_washing_machine(image: UploadFile = File(...)):
    """ Uploads a washing machine image and retrieves details from Gemini API """
    global washing_machine_info
    prompt = "This is an image of a washing machine. For this image, extract as much details as you can that can help a user to use it. Write less than three sentences."
    washing_machine_info = call_gemini_api(image, prompt)
    return {"message": "Washing machine details saved", "info": washing_machine_info}

# React code :
# const fetchWashingMachineInfo = async () => {
#     const response = await fetch("http://localhost:8000
# /get/washing-machine-info");
#     const data = await response.json();
#     console.log(data.washing_machine_info); // Display in frontend
# };

@app.post("/upload/dryer")
def upload_dryer(image: UploadFile = File(...)):
    """ Uploads a dryer image and retrieves details from Gemini API """
    global dryer_info
    prompt = "Upload an image of a dryer. For this image, extract as much details as you can that can help a user to use it. Write less than three sentences."
    dryer_info = call_gemini_api(image, prompt)
    return {"message": "Dryer details saved", "info": dryer_info}

@app.post("/upload/clothing-tag")
def upload_clothing_tag(image: UploadFile = File(...)):
    """ Uploads a clothing tag image and retrieves washing and drying instructions """
    if not washing_machine_info or not dryer_info:
        return {"error": "Please upload washing machine and dryer images first"}
    
    # Formulating prompt using previous image information
    prompt = ("This is a tag of a cloth. Retrieve the laundry symbols from this tag. "
              "Using the washing machine image and the dryer image uploaded before "
              "and the information retrieved from the most recent image of the clothing tag, "
              "give me one sentence instruction on how to use my washing machine "
              "and one sentence instruction on how to use my dryer.")
    
    instructions = call_gemini_api(image, prompt)
    clothing_tag_instructions.append(instructions)
    return {"message": "Clothing tag instructions saved", "instructions": instructions}

@app.get("/get/washing-machine-info")
def get_washing_machine_info():
    """ Returns the extracted washing machine details """
    return {"washing_machine_info": washing_machine_info}

@app.get("/get/dryer-info")
def get_dryer_info():
    """ Returns the extracted dryer details """
    return {"dryer_info": dryer_info}

@app.get("/get/clothing-tag-instructions")
def get_clothing_tag_instructions():
    """ Returns all extracted clothing tag instructions """
    return {"clothing_tag_instructions": clothing_tag_instructions}


