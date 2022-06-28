# myPyApi
Ini adalah API yang dibuat dengan Python dengan framework FastAPI. Pastikan mesinmu memiliki:
1. Python 3.*
2. Package Uvicorn  
````
pip install uvicorn
````
3. Package FastAPI  
````
pip install fastapi
````
4. Package Mysql Connector  
````
pip install mysql-connector-python
````
<br>
<br>
Tambahkan file db-prima sebagai file konfigurasi. File konfigurasi terdiri dari sebagai berikut.
1. ip untuk akses remote dari luar
2. ip untuk akses remote dari dalam(intranet)
3. nama user mysql
4. password user mysql
5. nama database yang digunakan
6. keterangan 'public' untuk akses dari luar dan 'local' untuk akses dari intranet.

Setelah siap ketikkan di terminal :<br>
````
uvicorn main:app --host 0.0.0.0 --reload --port 8001
````
Akses di browser dengan localhost:8001

<br>
<br>
<br>

## Aku menggunakan docker, bagaimana caranya ?
soon

<br>
<br>
Enjoy!


