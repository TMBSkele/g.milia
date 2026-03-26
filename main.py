from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


product_list = [
    {"name": "notebook DELL", "price": 500.00, "location" : "Cagliari"},
    {"name": "notebook HP", "price": 490.00, "location" : "Roma"},
    {"name": "notebook Lenovo", "price": 429.99, "location" : "Firenze"},
]


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Renders the home page.
    """
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"text": "Welcome to the store"}
    )

@app.get("/", response_class=HTMLResponse)
def products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"product_list": product_list}
    )