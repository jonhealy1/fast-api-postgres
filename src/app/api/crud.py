from app.api.models import NoteSchema
from app.db import database, notes


async def post(payload: NoteSchema):
    data_payload = payload.data
    # data_payload = json.loads(r'{"data": {"test": 1, "hello": "I have \" !"}, "id": 4}')
    query = notes.insert().values(
        title=payload.title,
        description=payload.description,
        geometry=payload.geometry,
        data=data_payload,
    )
    return await database.execute(query=query)


async def get(id: int):
    query = notes.select().where(id == notes.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = "SELECT notes.id, notes.title, notes.description, ST_AsText(geometry) AS geometry, notes.data FROM notes"
    return await database.fetch_all(query=query)


async def put(id: int, payload: NoteSchema):
    query = (
        notes.update()
        .where(id == notes.c.id)
        .values(
            title=payload.title,
            description=payload.description,
            geometry=payload.geometry,
        )
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = notes.delete().where(id == notes.c.id)
    return await database.execute(query=query)

# select * from notes where ST_Intersects(notes.geometry, 'POINT(0 1)');
async def search_location(x: int, y: int):
    query = f"select notes.id, notes.title, notes.description, ST_AsText(geometry) AS geometry, notes.data from notes where ST_Intersects(notes.geometry, 'POINT({x} {y})')"
    return await database.fetch_all(query=query)
