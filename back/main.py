from fastapi import FastAPI

from back.api.routes import routers

app = FastAPI()

for router in routers:
    app.include_router(router)


def run_dev_server():
    import uvicorn

    uvicorn.run("back.main:app", reload=True)


if __name__ == "__main__":
    run_dev_server()
