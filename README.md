**Project launch**
In order to launch the project, follow the the steps below:
1. Find the file **".env.template"** and remove **".template"** from the name of the file.
2. Inside tthe file set the environment variables:
    - **POSTGRES_USER** - name of PostgreSQL user
    - **POSTGRES_PASSWORD** - user's password for PostgreSQL
    - **POSTGRES_DB** - name of selected database
    - **POSTGRES_EXT_PORT** - PostgreSQL external port
3. In terminal run the following commands:
```powershell
docker compose build
docker compose up
```
4. Go to the browser and open the following link:
```http
http://127.0.0.1:8011/docs
```

**Launch tests**
In order to launch tests, after setting environment variables above, type in terminal (we need to create environment and install all dependencies):
```powershell
python -m venv venv
python venv\Scripts\activate (alternatively you can use venv\Scripts\Activate.ps1)
pip install -r requirements.txt
pytest -v
```