from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Optional
import PIL.Image
import google.generativeai as genai
import io  # For in-memory file handling

app = FastAPI()

# Configure the Gemini API
genai.configure(api_key="GEMINI_API_KEY")  

class LaundryAssistant:
    def __init__(self):
        self.washing_machine_info: Optional[str] = None
        self.dryer_info: Optional[str] = None
        self.clothing_tag_instructions: Optional[str] = None
    
    def call_gemini_api(self, image_bytes: bytes, prompt: str) -> str:
        """Sends image bytes and prompt to Gemini API."""
        try:
            image = PIL.Image.open(io.BytesIO(image_bytes))  # Open image from bytes
            model = genai.GenerativeModel(model_name="gemini-1.5.pro")  # Or your model name
            response = model.generate_content(prompt, image)  # Pass image object directly
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            raise HTTPException(status_code=500, detail=f"Gemini API Error: {e}")
    
    async def upload_image(self, image: UploadFile, prompt: str, storage_attr: str):
        """Handles image upload and Gemini API call."""
        try:
            image_bytes = await image.read()
            result = self.call_gemini_api(image_bytes, prompt)
            setattr(self, storage_attr, result)
            return {"message": f"{storage_attr.replace('_', ' ').title()} details saved", "info": result}
        except Exception as e:
            return {"error": str(e)}

laundry_assistant = LaundryAssistant()

@app.post("/upload/washing-machine")
async def upload_washing_machine(image: UploadFile = File(...)):
    return await laundry_assistant.upload_image(image, "This is a washing machine image. Extract details to help a user. (less than 3 sentences)", "washing_machine_info")

@app.post("/upload/dryer")
async def upload_dryer(image: UploadFile = File(...)):
    return await laundry_assistant.upload_image(image, "This is a dryer image. Extract details to help a user. (less than 3 sentences)", "dryer_info")

@app.post("/upload/clothing-tag")
async def upload_clothing_tag(image: UploadFile = File(...)):
    if not laundry_assistant.washing_machine_info or not laundry_assistant.dryer_info:
        raise HTTPException(status_code=400, detail="Upload washer and dryer images first")
    
    prompt = (f"This is a clothing tag. Extract laundry symbols. Given washing machine info:\n"
              f"{laundry_assistant.washing_machine_info}\nDryer info:\n{laundry_assistant.dryer_info}\n"
              "Give ONE SENTENCE washing and ONE SENTENCE drying instruction.")
    
    return await laundry_assistant.upload_image(image, prompt, "clothing_tag_instructions")

@app.get("/get/washing-machine-info")
async def get_washing_machine_info():
    return {"washing_machine_info": laundry_assistant.washing_machine_info}

@app.get("/get/dryer-info")
async def get_dryer_info():
    return {"dryer_info": laundry_assistant.dryer_info}

@app.get("/get/clothing-tag-instructions")
async def get_clothing_tag_instructions():
    return {"clothing_tag_instructions": laundry_assistant.clothing_tag_instructions}
