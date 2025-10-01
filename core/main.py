from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from schemas import BaseCheckSchema, CreateCostSchema
from typing import List
from uuid import uuid4

app = FastAPI()
storage = {}


@app.post('/costs', status_code=status.HTTP_201_CREATED, response_model=dict)
def create_cost(cost: CreateCostSchema):
    new_id = str(uuid4())
    storage[new_id] = {"id": new_id, **cost.model_dump()}
    content = {"message": "New cost added.", "id": new_id}
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@app.get('/costs', status_code=status.HTTP_200_OK, response_model=List[BaseCheckSchema])
def getting_costs():
    return list(storage.values())


@app.get('/costs/{num_id}', status_code=status.HTTP_200_OK, response_model=BaseCheckSchema)
def get_by_id(num_id: str):
    if num_id in storage:
        return storage[num_id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='ID not found'
        )


@app.put('/costs/{num_id}', status_code=status.HTTP_200_OK, response_model=dict)
def update_info(num_id:str, cost: CreateCostSchema):
    if num_id in storage:
        storage[num_id] = {"id": num_id, **cost.model_dump()}
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
