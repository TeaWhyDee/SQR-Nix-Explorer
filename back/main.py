from fastapi import FastAPI

from back.api.routes import routers


def get_app(debug=False):
    app = FastAPI(debug=debug, title="Nix Explorer")
    for router in routers:
        app.include_router(router)
    return app


def run_dev_server():
    import uvicorn

    uvicorn.run("back.main:get_app", reload=True, factory=True)


if __name__ == "__main__":
    run_dev_server()
