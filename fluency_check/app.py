from fastapi import FastAPI
import uvicorn
import pickle
from model import fluent

app = FastAPI()

test_model = pickle.load(open('C:/Users/rohan/Desktop/Work/proj/english-ui/fluency_check/mlp_300_32.sav', 'rb'))

@app.get("/{name}")
def hello(name):
    return {"hello {} and welcome to this api".format(name)}

@app.get("/")
def greet():
    return {"Hello World"}

@app.post("/predict")
def predict(req: fluent):
    m0 = req.n_mfcc0
    m1 = req.n_mfcc1
    m2 = req.n_mfcc2
    m3 = req.n_mfcc3
    m4 = req.n_mfcc4
    m5 = req.n_mfcc5
    m6 = req.n_mfcc6
    m7 = req.n_mfcc7
    m8 = req.n_mfcc8
    m9 = req.n_mfcc9
    m10 = req.n_mfcc10
    m11 = req.n_mfcc11
    m12 = req.n_mfcc12
    m13 = req.n_mfcc13
    m14 = req.n_mfcc14
    m15 = req.n_mfcc15
    m16 = req.n_mfcc16
    m17 = req.n_mfcc17
    m18 = req.n_mfcc18
    m19 = req.n_mfcc19
    rm = req.rmse
    sf = req.spectral_flux
    zcr = req.zcr
    features = list([m0, m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,rm,sf,zcr])
    predict = test_model.predict([features])
    return predict



if __name__=="__main__":
    uvicorn.run(app)
