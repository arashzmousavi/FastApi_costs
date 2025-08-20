from fastapi import FastAPI, HTTPException, status
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
    return {'id': new_id, 'item': storage[new_id]}

@app.get('/costs', status_code=status.HTTP_200_OK)
def getting_costs():
    return storage

@app.get('/costs/{num_id}', status_code=status.HTTP_200_OK)
def retrive_by_id(num_id:str):
    if num_id in storage:
        return storage[num_id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='ID not found'
        )
    
@app.put('/costs/{num_id}', status_code=status.HTTP_200_OK)
def update_info(num_id:str, desc:str, amount:float):
    if num_id in storage:
        storage[num_id]['description'] = desc
        storage[num_id]['amount'] = amount
        return {
            'msg': 'Update successfully',
            'item': storage[num_id]
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID not found"
        )

# DELETE: deleting specific cost by id
@app.delete('/costs/{num_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_content(num_id:str):
    if num_id in storage:
        del storage[num_id]
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="ID not found"
    )
