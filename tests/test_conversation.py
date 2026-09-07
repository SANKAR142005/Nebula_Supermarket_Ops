from app.modules.conversation import save_chat,load_chat
def test_chat(tmp_path): save_chat('abc',[{'role':'user','content':'hi'}]); assert load_chat('abc')[0]['content']=='hi'
