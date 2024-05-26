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

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="MyTools API",
    description="API para a aplicação MyTools",
    version="0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    debug=True
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/qrcode")
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


@app.post("/removebg")
@limiter.limit("40/minute")
async def remove_background(request: Request, image: UploadFile):
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
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)



