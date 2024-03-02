<h1>A FastAPI Model Driven Service  </h1>

<h3>Database:</h3>
<h4>RavenDB - A nosql ACID compliant cluster db.</h4>


<br/>
<br/>
<br/>

<h1>To Run:</h1>

**You can use the provided instance of ravendb**
**Or get your own here**
- *<a href="https://ravendb.net/download">https://ravendb.net/download</a>*

**Install and run ollama from on your mac**
- *<a href="https://ollama.ai">https://ollama.ai/</a>*


**Edit .env file in root with your raven db url**
- `BASE_DB_URL=http://127.0.0.1:2222` 


**On first run in the project root, create your conda env:**
- `conda create --name <my-env>`


**Activate venv by running from the root of this project:**
  - `conda activate ./.conda`


**After activating your conda env, from root `cd be` and Install deps with:**
- `pip3 install requirements.txt`
- `pip3 install "python-jose[cryptography]" v = 3.4.0`
- `pip3 install "passlib[bcrypt]" v = 4.0.1`



<br/>
<br/>
<br/>

<h1>To start the project</h1>

**1. In a terminal window from the `db` package run to start the db**
- `./run.sh`

**2. In another terminal window with the activated conda env `cd` into the `be/src` package and run**
- `python3 main.py`



The api is now running, you can access the swagger docs at <a href="http://0.0.0.0:8080/docs">`http://0.0.0.0:8080/docs`</a>

You can also use pnpm to install and use the FE UI to interface with ollama. You must start ollama on your machine and install the llama model before starting the fastApi server that runs in main.py


**Todos**

Adjust so util files only use functions, no need for classes. Explore separation into another module so we can import static single instances of it.

Find a tool to analyze the performance of the code when hit with a ton of concurrent requests.
- Maybe this tool https://locust.io/


Find a better way to provide context to down stream methods, options works for middlware but what about filtering from model in repository? Spring provides flat later we can grab and pull from, is there a python equivilant? Or perhaps some sort of "Store" that is request based that allows us to set context on a per request basis... maybe I can use a session cookie for this?
