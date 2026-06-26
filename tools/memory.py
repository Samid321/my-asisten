from langchain.tools import tool

@tool
def baca_memory():
    """Ini adalah tool yang wajib dijalankan pertama kali untuk mengakses ingatan dan cukup 1 kali pengunaan saja"""
    with open('./memory/memory.txt','r') as file:
        return file.read()
@tool 
def simpan_memory(ekstrak_percakapan:str)->str:
    """ini adalah tools yang di gunakan untuk menyimpan data, yang berasal dari ekstrakan percakapan kita"""
    try:
        with open('./memory/memory.txt','a') as  file:
            file.write(f"\n{ekstrak_percakapan}")
            return """data sudah di isi bang"""
    except FileNotFoundError:
        with open('./memory/memory.txt','w') as file:
            file.write(ekstrak_percakapan)
    except Exception as e:
        return e
        

