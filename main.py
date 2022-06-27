from fastapi import FastAPI
import emr

app = FastAPI()

@app.get("/") 
async def root():
    return {"message": "Hello World"}

@app.get("/next/") 
async def root():
    return {"message": "Next"}

@app.get("/mr_result/{type_search}/{value}") 
async def read_item(type_search:str,value:str):
    v = value
    def f(t):
      return {
        'no_rm':emr.get_erm_result_from_RM(v),
        'no_reg':emr.get_erm_result_from_NOREG(v)
      }.get(t,emr.get_erm_result_from_DR(v))

    return f(type_search)