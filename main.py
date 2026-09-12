import base64
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Mount the static directory so CSS/JS/Images load correctly
app.mount("/static/", StaticFiles(directory="static"), name="static")

# Ensure a directory exists to store captured photos
os.makedirs("saved_photos", exist_ok=True)

# JSON Data representing your connections log
CONNECTIONS_DATABASE = [
    {
        "id": "0928",
        "type": "formal",
        "type_label": "FORMAL PROFILE",
        "time": "JUST NOW",
        "name": "ELENA ROSTOVA",
        "title": "VP OF PRODUCT ENGINEERING",
        "company": "VEKTOR LABS",
        "email": "elena@vektor.io",
        "phone": "+1 (415) 890-2134",
        "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=faces",
        "info_boxes": {
            "working_on": "Currently architecting distributed spatial computing & tactile neural vision networks at Vektor Labs. Launching v2.4 this Q3 with real-time hand-tracking synchronization.",
            "stack": "Specialized in systems engineering with Rust and C++, high-throughput neural pipelines using Python and PyTorch, alongside reactive frontend interfaces built in TypeScript, React, WebGPU, and CUDA.",
            "proud_of": "Building the sub-10ms neural tactile processing engine from scratch, enabling seamless zero-calibration spatial interaction across heterogeneous hardware.",
            "philosophy": "Ruthless simplification over premature abstraction. Direct, low-latency communication loops both in silicon architecture and engineering teams."
        }
    }
]

@app.get("/api/connections")
def get_connections():
    return CONNECTIONS_DATABASE

@app.post("/api/save-photo")
async def save_photo(request: Request):
    data = await request.json()
    image_data = data.get("image")
    
    if not image_data:
        return {"status": "error", "message": "No image data found"}
    
    # Strip the base64 header (e.g., 'data:image/png;base64,')
    encoded_data = image_data.split(",")[1]
    decoded_image = base64.b64decode(encoded_data)
    
    # Define file path to save inside saved_photos directory
    file_path = "saved_photos/capture.png"
    
    with open(file_path, "wb") as fh:
        fh.write(decoded_image)
        
    return {"status": "success", "message": "Photo saved successfully on server!"}

@app.get("/")
def read_scan():
    return FileResponse("static/index/index.html")

@app.get("/network")
def read_network():
    return FileResponse("static/network/index.html")

@app.get("/formal_cards")
def read_cards():
    return FileResponse("static/formal_cards/index.html")