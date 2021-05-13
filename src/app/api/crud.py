from app.api.models import NoteSchema
from app.db import notes, database
import json

async def post(payload: NoteSchema):
    data_payload = payload.data
    # data_payload = json.loads(r'{"data": {"test": 1, "hello": "I have \" !"}, "id": 4}')
    query = notes.insert().values(title=payload.title, description=payload.description, geometry=payload.geometry, data=data_payload)
    return await database.execute(query=query)

async def get(id: int):
    query = notes.select().where(id == notes.c.id)
    return await database.fetch_one(query=query)

async def get_all():
    # query = notes.select()

    query = "SELECT notes.id, notes.title, notes.description, ST_AsText(geometry) AS geometry, notes.data FROM notes"
    # query = notes.select().where(notes.c.geometry.to_right('POLYGON((0 0,1 0,1 1,0 1,0 0))'))
    # query = notes.select().where(notes.c.geometry.to_right('POINT(1.1 0.4)'))
    # query = notes.select().where(notes.c.geometry.distance_box('POINT(0 0)') > 1)
    # query = notes.select().where(notes.c.geometry.contains('POINT(0 0)'))
    # query = notes.select().where(notes.c.geometry.ST_Intersects('LINESTRING(2 1,4 1)'))
    return await database.fetch_all(query=query)

async def put(id: int, payload: NoteSchema):
    query = (
        notes
        .update()
        .where(id == notes.c.id)
        .values(title=payload.title, description=payload.description, geometry=payload.geometry)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)

async def delete(id: int):
    query = notes.delete().where(id == notes.c.id)
    return await database.execute(query=query)