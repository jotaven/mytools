from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import io
from PIL import Image
import rembg
import qrcode
import numpy as np

app = FastAPI(
    title="MyTools API",
    description="API para a aplicação MyTools",
    version="0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)
 
@app.post("/qrcode")
async def generate_qr_code(url: str):
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


@app.get("/removebg")
async def remove_background(image: UploadFile):
    if image.content_type not in ["image/jpeg", "image/png"]:
        return HTTPException(status_code=400, detail="Error! Invalid file format.")
    if image.content_length == 0:
        return HTTPException(status_code=400, detail="Error! Empty file.")
    if image.content_length is None:
        return HTTPException(status_code=400, detail="Error! File not provided.")
    try:
        image = Image.open(image.file)
        image = np.array(image)
        output = rembg.remove(image)
        img = Image.fromarray(output)
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)



