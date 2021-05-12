from pydantic import BaseModel, Field
from typing import List, Any

'''
curl -X 'POST' \
  'http://localhost:8002/notes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "helllo",
  "description": "hihi",
  "geometry": "POLYGON((0 0,1 0,1 1,0 1,0 0))"
}'
'''

class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    geometry: Any
class NoteDB(NoteSchema):
    id: int