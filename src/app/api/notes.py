import json
from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.api.models import NoteDB, NoteSchema

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note_id = await crud.post(payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
        "geometry": payload.geometry,
    }
    return response_object


@router.get("/{id}/", response_model=NoteDB)
async def read_note(
    id: int = Path(..., gt=0),
):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await crud.get_all()


@router.put("/{id}/", response_model=NoteDB)
async def update_note(
    payload: NoteSchema,
    id: int = Path(..., gt=0),
):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await crud.put(id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
        "geometry": payload.geometry,
    }
    return response_object


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return note

@router.get("/search/{x}{y}/", response_model=List[NoteDB])
async def search(
    x: int,
    y: int
):
    note = await crud.search_location(x, y)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# select data->>'address' from notes;
@router.get("/jsonb/{search_param}")
async def search_jsonb(
    search_param: str
):
    # return await crud.search_jsonb(search_param)
    response = await crud.search_jsonb(search_param)
    address_list = []
    for r in response:
        if r["?column?"] is not None:
            parsed_data = json.loads(r["?column?"].replace("\'", '"'))
            address_list.append(parsed_data)
        # json.loads(response_read.replace("\'", '"'))

    return address_list