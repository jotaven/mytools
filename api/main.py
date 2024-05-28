from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import io
from PIL import Image
import rembg
import qrcode
import numpy as np
import cv2

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="MyTools API",
    description="API para a aplicação MyTools",
    version="1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    debug=True
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def get_image(image: UploadFile):
    image = Image.open(image.file)
    image = np.array(image)
    return image

@app.get("/api/qrcode")
@limiter.limit("120/minute")
async def generate_qr_code(request: Request, url: str):
    url=url.strip()
    if url == "":
        return HTTPException(status_code=400, detail="Error! URL not provided.")
    try:
        img = qrcode.make(url, border=2)
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/api/removebg")
@limiter.limit("40/minute")
async def remove_background(request: Request, image: UploadFile):
    try:
        image = get_image(image)
        output = rembg.remove(image)
        img = Image.fromarray(output)
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@app.post("/api/contour")
async def image_contour(request: Request, image: UploadFile):
    try:
        image = get_image(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 30, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        image = cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 3)
        img_byte_array = io.BytesIO()
        img = Image.fromarray(image)
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/api/scketch")
async def image_scketch(request: Request, image: UploadFile):
    try:
        image = get_image(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)
        image = cv2.divide(gray, gray_blur, scale=256)
        img_byte_array = io.BytesIO()
        img = Image.fromarray(image)
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/api/img2gray")
async def image_scketch(request: Request, image: UploadFile):
    try:
        image = get_image(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_byte_array = io.BytesIO()
        img = Image.fromarray(gray)
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/api/threshold1")
async def image_threshold1(request: Request, image: UploadFile):
    try:
        image = get_image(image)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img_byte_array = io.BytesIO()
        img = Image.fromarray(threshold)
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.post("/api/threshold2")
async def image_threshold2(request: Request, image: UploadFile):
    try:
        image = get_image(image)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5) 
        img_byte_array = io.BytesIO()
        img = Image.fromarray(threshold)
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)



