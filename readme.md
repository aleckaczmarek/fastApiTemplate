fastapi model based service repo data store with ravendb as nosql data store

**to run:**
**you will need ravendb**
- *https://ravendb.net/download*

**edit .env file in root with your  raven db url**
- *BASE_DB_URL=http://127.0.0.1:2222 *

**Activate venv with:**

- conda activate ~/Path_To_Folder/.conda

**Install deps with:**

- pip3 install requirements.txt
- pip3 install "python-jose[cryptography]" v = 3.4.0
- pip3 install "passlib[bcrypt]" v = 4.0.1
