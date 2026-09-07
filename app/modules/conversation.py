import json
from app.storage.connection import SessionFactory
from app.storage.entities import ChatState

def load_chat(channel_id):
    db=SessionFactory()
    try:
        row=db.query(ChatState).filter_by(channel_id=str(channel_id)).first(); return json.loads(row.transcript) if row and row.transcript else []
    finally: db.close()

def save_chat(channel_id,history):
    db=SessionFactory()
    try:
        row=db.query(ChatState).filter_by(channel_id=str(channel_id)).first()
        if not row: row=ChatState(channel_id=str(channel_id)); db.add(row)
        row.transcript=json.dumps(history[-30:]); db.commit()
    finally: db.close()
