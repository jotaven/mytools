from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import io
from PIL import Image
import rembg
import qrcode
import base64

app = FastAPI()
 
@app.get("/qrcode")
async def generate_qr_code(url: str):
    try:
        url=url.strip()
        if url == "":
            return HTTPException(status_code=400, detail="Error! URL not provided.")
        img = qrcode.make()
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

