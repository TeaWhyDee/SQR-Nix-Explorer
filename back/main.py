from fastapi import FastAPI, HTTPException

app = FastAPI()


# TODO: Add return types to all
# TODO: Add auth


# ===== USER =====
@app.post("/register")
def register(username: str, password: str):
    return "Not Implemented"


@app.post("/login")
def login(username: str, password: str):
    return "Not Implemented"


@app.post("/logout")
def logout():
    return "Not Implemented"


# ===== STORES =====
@app.post("/add_store")
def add_store(store_name: str):
    # Check for auth etc

    raise HTTPException(status_code=500, detail="Not implemented")

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

    return {"package_exists": True}
    raise HTTPException(status_code=500, detail="Not implemented")


@app.get("/store/get_difference_paths")
def get_difference_of_paths(store_name1: str, store_name2: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@app.get("/store/get_difference_package_closures")
def get_difference_of_package_closures(package1: str, package2: str):
    # ex: store1#bash,  store2#hello
    raise HTTPException(status_code=500, detail="Not implemented")


