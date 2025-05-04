from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import sqlite3
import os
from routers.auth import auth_router
from routers.google_sheets.router import sheets_router
from expense import ExpenseResponse


from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
port = 9090




app = FastAPI()


app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")
templates = Jinja2Templates("frontend/dist")



app.include_router(auth_router, prefix="/auth")
app.include_router(sheets_router, prefix="/expenses")
# Enable CORS

app.add_middleware(
    CORSMiddleware,
    # allow_origins=[""],  # Replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
from init_db_ import init_db
# Call init_db at startup
init_db()

from auth_baseModels import UserCreate, UserLogin



@app.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses():
    return []


@app.get("/", response_model=List[ExpenseResponse])
def get_expenses(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/categories")
def get_categories():
    return [
        "Food", "Gifts", "Health/medical", "Home", "Transportation", 
        "Personal", "Pets", "Utilities", "Travel", "Debt", "Other"
    ]



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)