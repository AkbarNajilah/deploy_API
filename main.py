#import libary 
from fastapi import FastAPI, HTTPException, Header
import pandas as pd
#create object
app = FastAPI()

#create API key 
API_KEY = "kepoya"

# create endpoint
@app.get("/")
def home():
    return {"message": "Selamat datang di toko saya"}

#create endpoint lagi 
@app.get("/data")
def read_data():
    #untuk baca data dari file csv 
    df = pd.read_csv("data.csv")
    #convert dataframe to dictionary with orient="records" for each row 
    return df.to_json(orient="records")

#buat endpoint untuk memangil parameter
@app.get("/data/{number_id}")
def read_item(number_id: int):
    #read data from csv 
    df = pd.read_csv("data.csv")

    #filter data by ID
    filter_data = df[df["id"] == number_id]
    
    if len(filter_data) == 0:
        raise HTTPException(status_code=404,detail="Barang nya gaada nih, coba cari barang lain ")
    #convert dataframe to dictionary with orient="records" for each row
    return filter_data.to_dict(orient="records")

#create endpoint update file data
@app.put("/items/{number_id}")
def update_item(number_id: int, nama_barang: str, harga: float):
    #read data from csv 
    df = pd.read_csv("data.csv")
    
    #create dafatframe from update input
    updated_df = pd.DataFrame({
        "id":number_id,
        "nama_barang":nama_barang,
        "harga":harga
        }, index=[0])

    #merge update dataframe with original dataframe
    merged_df = pd.concat([df,updated_df], ignore_index=True)

    #save updated dataframe to file csv
    merged_df.to_csv("data.csv", index=False)
    
    return{"message" :f"Item with ID {number_id} has been updated successfully."}

@app.get("/secret")
def read_secret(api_key: str = Header(None)):
    #read data from csv 
    secret_df = pd.read_csv("secret_data.csv")
  
    #cek apakah api_key nya valid
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="AHAHAAHA mampus gabisa masuk :)")
    
    return secret_df.to_dict(orient="records")