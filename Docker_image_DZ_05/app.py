from fastapi import FastAPI, status
import uvicorn

app = FastAPI()


@app.get('/')
async def base_page():
    return {"message": "Hello!"}


@app.get('/ping/', status_code=status.HTTP_200_OK)
async def view():
    return {"message": "pong"}


if __name__ == '__main__':
    uvicorn.run('app:app', host="127.0.0.1", port=8000, reload=True)
