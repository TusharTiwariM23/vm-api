from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

# Database connection details (Update with actual PostgreSQL credentials)
DB_HOST = os.getenv("DB_HOST", "192.168.56.103")  # Use PostgreSQL VM IP
DB_NAME = os.getenv("DB_NAME", "cars_db")
DB_USER = os.getenv("DB_USER", "api_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "82338233")

# Connect to the PostgreSQL database
def get_db_connection():
    return psycopg2.connect(
        host="192.168.56.103",
        database="cars_db",
        user="api_user",
        password="82338233",
        cursor_factory=RealDictCursor
    )
# Define the request model for input validation
class Car(BaseModel):
    car_serial_no: int
    car_name: str
    car_price: float

@app.get("/")
def read_root():
    return {"message": "FastAPI running on appvm"}

@app.get("/items")
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars;")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"items": items}

# **POST endpoint to add a new car**
@app.post("/add-car")
def add_car(car: Car):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if car_serial_no already exists
    cursor.execute("SELECT * FROM cars WHERE car_serial_no = %s;", (car.car_serial_no,))
    existing_car = cursor.fetchone()

    if existing_car:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Car with this serial number already exists")

    # Insert the new car record
    cursor.execute(
        "INSERT INTO cars (car_serial_no, car_name, car_price) VALUES (%s, %s, %s);",
        (car.car_serial_no, car.car_name, car.car_price)
    )
    conn.commit()

    cursor.close()
    conn.close()
    return {"message": f"Car '{car.car_name}' added successfully"}

# **PUT endpoint to update an existing car by serial number**
@app.put("/update-car/{car_serial_no}")
def update_car(car_serial_no: int, car: Car):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the car exists
    cursor.execute("SELECT * FROM cars WHERE car_serial_no = %s;", (car_serial_no,))
    existing_car = cursor.fetchone()

    if not existing_car:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Car not found")

    # Update the car details
    cursor.execute(
        "UPDATE cars SET car_name = %s, car_price = %s WHERE car_serial_no = %s;",
        (car.car_name, car.car_price, car_serial_no)
    )
    conn.commit()

    cursor.close()
    conn.close()
    return {"message": f"Car with serial number {car_serial_no} updated successfully"}

# **DELETE endpoint to remove a car by name**
@app.delete("/delete-car/{car_name}")
def delete_car(car_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the car exists
    cursor.execute("SELECT * FROM cars WHERE car_name = %s;", (car_name,))
    car = cursor.fetchone()

    if not car:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="No record found")

    # Delete the car if found
    cursor.execute("DELETE FROM cars WHERE car_name = %s;", (car_name,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": f"Car '{car_name}' deleted successfully"}