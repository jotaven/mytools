from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel, Field
from typing import Optional
from PIL import Image
import qrcode

app = FastAPI()

class Url(BaseModel):
    url: str = Field(..., example="https://example.com")

@app.post("/qrcode")
async def generate_qr_code(url: Url):
    try:
        img = qrcode.make(url.url)
        filename = "qrcode.png"
        img.save("./" + filename)
        return {"message": "QR code generated successfully!", "qrcode": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.post("/img2gray")
async def img2gray(image: UploadFile = File(...)):
    try:
        img = Image.open(image)
        img = img.convert("L")
        filename = "gray_image.png"
        img.save("./" + filename)
        return {"message": "Image converted to grayscale successfully!", "gray_image": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

