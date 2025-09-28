from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from uuid import uuid4


app = FastAPI()
storage = {}


@app.post('/costs', status_code=status.HTTP_201_CREATED)
def create_cost(desc:str, amount:float):
    new_id = str(uuid4())
    storage[new_id] = {
        'description': desc,
        'amount': amount
    }
    content = {"message": f"New cost ({new_id}) added."}
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@app.get('/costs', status_code=status.HTTP_200_OK)
def getting_costs():
    return JSONResponse(content=storage, status_code=status.HTTP_200_OK)


@app.get('/costs/{num_id}', status_code=status.HTTP_200_OK)
def get_by_id(num_id:str):
    if num_id in storage:
        return JSONResponse(content=storage[num_id], status_code=status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='ID not found'
        )
    

@app.put('/costs/{num_id}', status_code=status.HTTP_200_OK)
def update_info(num_id:str, desc:str, amount:float):
    if num_id in storage:
        storage[num_id]['description'] = desc
        storage[num_id]['amount'] = amount
        content = {"message": f"Update ({num_id}) successfully"}
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ID not found"
    )


@app.delete('/costs/{num_id}', status_code=status.HTTP_200_OK)
def delete_content(num_id:str):
    if num_id in storage:
        del storage[num_id]
        content = {"message": f"Cost-ID ({num_id}) deleted."}
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ID not found"
    )
