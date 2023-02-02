from fastapi import FastAPI
import uvicorn
import pickle
from model import fluent
import numpy as np
import pandas as pd

app = FastAPI()

pickle_in = open("./mlp_300_32.sav", "rb")
test_model = pickle.load(pickle_in)
# test_model = pickle.load(open('mlp_300_32.pkl', 'rb'))

@app.get("/{name}")
def hello(name):
    return {"hello {} and welcome to this api".format(name)}

@app.get("/")
def greet():
    return {"Hello World"}

@app.post("/predict")
def predict(data: fluent):
    data = data.dict()
    m0 = data['n_mfcc0']
    m1 = data['n_mfcc1']
    m2 = data['n_mfcc2']
    m3 = data['n_mfcc3']
    m4 = data['n_mfcc4']
    m5 = data['n_mfcc5']
    m6 = data['n_mfcc6']
    m7 = data['n_mfcc7']
    m8 = data['n_mfcc8']
    m9 = data['n_mfcc9']
    m10 = data['.n_mfcc10']
    m11 = data['.n_mfcc11']
    m12 = data['.n_mfcc12']
    m13 = data['.n_mfcc13']
    m14 = data['.n_mfcc14']
    m15 = data['.n_mfcc15']
    m16 = data['.n_mfcc16']
    m17 = data['n_mfcc17']
    m18 = data['n_mfcc18']
    m19 = data['n_mfcc19']
    rm = data['rmse']
    sf = data['spectral_flux']
    zcr = data['zcr']
    # features = list([m0, m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,rm,sf,zcr])
    prediction = test_model.predict([[m0, m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,rm,sf,zcr]])
    return prediction



if __name__=="main__":
    uvicorn.run(app)
