fastapi model based service repo data store with ravendb as nosql data store

**to run:**
**you will need ravendb**
- *https://ravendb.net/download*

**edit .env file in root with your  raven db url**
- *BASE_DB_URL=http://127.0.0.1:2222 *

**Activate venv with:**

  - conda activate ~/Path_To_Folder/.conda
  - 
  - conda activate ~/Desktop/macroMapper/.conda

**Install deps with:**

- pip3 install requirements.txt
- pip3 install "python-jose[cryptography]" v = 3.4.0
- pip3 install "passlib[bcrypt]" v = 4.0.1

 
 

**Todos**

Adjust so util files only use functions, no need for classes. Explore separation into another module so we can import static single instances of it.

Find a tool to analyze the performance of the code when hit with a ton of concurrent requests.

Find a better way to provide context to down stream methods, options works for middlware but what about filtering from model in repository? Spring provides flat later we can grab and pull from, is there a python equivilant? Or perhaps some sort of "Store" thats request based that allows us to set context on a per request basis... maybe ip ? hmm needs more thought.

- Maybe this tool https://locust.io/
