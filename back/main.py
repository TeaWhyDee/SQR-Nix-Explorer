from fastapi import FastAPI, HTTPException
from back import nix

app = FastAPI()


# TODO: Add return types to all
# TODO: Add auth


# ===== USER =====
@app.post("/register")
def register(username: str, password: str):
    # Add simple password validation
    raise HTTPException(status_code=500, detail="Not implemented")


@app.post("/login")
def login(username: str, password: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@app.post("/logout")
def logout():
    raise HTTPException(status_code=500, detail="Not implemented")


# ===== STORES =====
@app.post("/add_store")
def add_store(store_name: str):
    # Check for auth etc
    # Check that store doesn't already exist
    
    # TODO: Check for exceptions from nix
    # Probably call like this?
    try:
        nix.add_store(store_name)
    except Exception:
        pass

    raise HTTPException(status_code=500, detail="Not implemented")

    # Returns look similar to this:
    # return {"message": "Store registered successfully"}
    # raise HTTPException(status_code=401, detail="User not logged in")


@app.post("/remove_store")
def remove_store(store_name: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@app.post("/store/add_package")
def add_package_to_store(store_name: str, package_name: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@app.post("/store/remove_package")
def remove_package_from_store(store_name: str, package_name: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@app.get("/store/check_package_exists")
def check_package_exists(store_name: str, package_name: str):
    # return {"package_exists": True}
    raise HTTPException(status_code=500, detail="Not implemented")


@app.get("/store/get_difference_paths")
def get_difference_of_paths(store_name1: str, store_name2: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@app.get("/store/get_difference_paths")
def get_difference_of_package_closures(package1: str, package2: str):
    # ex: store1#bash,  store2#hello
    raise HTTPException(status_code=500, detail="Not implemented")


def run_dev_server():
    import uvicorn

    uvicorn.run("back.main:app", reload=True)


if __name__ == "__main__":
    run_dev_server()
