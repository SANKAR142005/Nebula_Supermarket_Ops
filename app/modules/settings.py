from app.storage.connection import SessionFactory
from app.storage.entities import UserSetting

def save_setting(key,value):
    db=SessionFactory(); key=key.strip().lower()
    try:
        row=db.query(UserSetting).filter_by(key=key).first()
        if row: row.value=str(value)
        else: db.add(UserSetting(key=key,value=str(value)))
        db.commit(); return {'success':True,'message':f'{key} saved.','key':key,'value':str(value)}
    finally: db.close()

def read_setting(key):
    db=SessionFactory()
    try:
        row=db.query(UserSetting).filter_by(key=key.strip().lower()).first()
        return {'success':True,'value':row.value if row else None}
    finally: db.close()

def all_settings():
    db=SessionFactory()
    try: return {'success':True,'settings':{x.key:x.value for x in db.query(UserSetting).all()}}
    finally: db.close()

def remove_setting(key):
    db=SessionFactory()
    try:
        row=db.query(UserSetting).filter_by(key=key.strip().lower()).first()
        if not row: return {'success':False,'message':'Setting not found.'}
        db.delete(row); db.commit(); return {'success':True,'message':'Setting removed.'}
    finally: db.close()
