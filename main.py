from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from pydantic import Field

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

@app.get("/products", response_class=HTMLResponse)
def products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"product_list": product_list}
    )

@app.get("/product_form", response_class=HTMLResponse)
def product_form(
        request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="product_form.html"
    )

@app.get("/insert_product", response_class=HTMLResponse)
def insert_product(
        name: Annotated[str, Field(min_length=2, max_length=30)],
        price: Annotated[float, Field(gt=0)],
        location: Annotated[str, Field(min_length=2, max_length=30)],
):
        product = {"name": name, "price": price, "location": location}
        product_list.append(product)
        return "Product added successfully"
