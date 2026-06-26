import os
from langchain.tools import tool,ToolRuntime
from dataclasses import dataclass
@dataclass
class file:
    file:str
@tool
def tambah_html_body(nama_file:str,kode:str):
    """
    Penting:selalu lakukan baca_kode terlebih dahulu
    Tambah kode sebelum </body>
    """

    with open(f"./workspace/{nama_file}") as f:
        html=f.read()


    html=html.replace(
        "</body>",
        kode + "\n</body>"
    )


    with open(f"./workspace/{nama_file}","w") as f:
        f.write(html)


    return "selesai"
    

@tool
def check_workspace() -> str:
    """
    Mengecek isi folder workspace.
    Return: list file jika ada, atau pesan jika kosong.
    """
    try:
        folder_path = './workspace'
        files = os.listdir(folder_path)
        if len(files) == 0:
            return "workspace kosong"
        return str(files)
    except Exception as e:
        return f"error: {str(e)}"

@tool
def Baca_file(nama_file: str) -> str:
    """Tool yang digunakan untuk membaca seluruh isi file."""
    try:
        with open(f'./workspace/day-67-starting-files-upgraded-blog/template/{nama_file}', 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"error: {str(e)}"

@tool
def Buat_file(nama_file: str, isi: str) -> str:
    """Tool yang digunakan untuk membuat file baru dari nol di dalam workspace."""
    try:
        with open(f"./workspace/{nama_file}", 'w', encoding='utf-8') as file:
            file.write(isi)
        return "file berhasil dibuat"
    except Exception as e:
        return f"error: {str(e)}"

@tool
def isi_data(nama_file: str, isi : str) -> str:
    """
    Tool yang digunakan untuk mengisi atau menambahkan kode baru di paling akhir file.
    Penting: Sebelum menggunakan tool ini harus jalankan tool Baca_file terlebih dahulu.
    """
    try:
        with open(f"./workspace/day-67-starting-files-upgraded-blog/template/{nama_file}", 'a', encoding='utf-8') as file:
            # Berikan enter baru sebelum menambahkan data agar tidak menempel
            file.write("\n" + isi)
        return "file berhasil diupdate di baris paling akhir"
    except Exception as e:
        return f"error: {str(e)}"

@tool
def tambah_data_setelah(nama_file: str, teks_penanda: str, isi : str) -> str:
    """ 
    Penting: sebelum mengunakan tool ini jalankan tool Baca_file dulu untuk memastikan teks_penanda tertulis persis sama.
    jika data merupakan kode html maka kode baru di buat setelah > dari teks penanda dan cukup 1  terlebih dahulu
    Tool untuk menambahkan/menyisipkan kode baru TEPAT SETELAH blok teks atau fungsi tertentu.
    Sangat berguna untuk menyisipkan fungsi di tengah-tengah file tanpa merusak kode lain.
    """
    try:
        with open(f"./workspace/day-67-starting-files-upgraded-blog/template/{nama_file}", 'r', encoding='utf-8') as file:
            content = file.read()
        
        if teks_penanda not in content:
            return f"error: Teks penanda '{teks_penanda}' tidak ditemukan di dalam file."
        
        teks_target = teks_penanda + "\n" + isi
        updated_content = content.replace(teks_penanda, teks_target)
        
        with open(f"./workspace/day-67-starting-files-upgraded-blog/template/{nama_file}", 'w', encoding='utf-8') as file:
            file.write(updated_content)
        return f"Berhasil menambahkan kode baru setelah: '{teks_penanda}'"
    except Exception as e:
        return f"error: {str(e)}"


@tool
def update_file(nama_file:str, isi:str)->str:
    """
    Mengubah isi file yang sudah ada.
    Gunakan setelah membaca file.
    """
    with open(f"./workspace/day-67-starting-files-upgraded-blog/template/{nama_file}", "w") as file:
        file.write(isi)

    return f"{nama_file} berhasil diperbarui"