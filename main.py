from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def calculate_bulbs(length: int, width: int, height: int, room_type: str) -> int:
    room_types = {
        'офис общего назначения': 300,
        'офис для чертежных работ': 500,
        'зал для конференций': 200,
        'переговорная комната': 200,
        'эскалатор': 100,
        'лестница': 100,
        'холл': 75,
        'коридор': 75,
        'архив': 75,
        'подсобные помещения': 50,
        'кладовая': 50
    }

    t = room_types.get(room_type, 0)
    k = t * length * width * height // 700
    if t * length * width * height / 700 - k > 0:
        k += 1
    return k

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, length: int = Form(...), width: int = Form(...), height: int = Form(...), room_type: str = Form(...)):
    result = calculate_bulbs(length, width, height, room_type)
    return templates.TemplateResponse("form.html", {"request": request, "result": result})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
