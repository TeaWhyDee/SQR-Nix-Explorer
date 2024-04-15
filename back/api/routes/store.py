from fastapi import APIRouter, HTTPException

from back import nix

store = APIRouter(prefix="/store")


@store.post("/add_store")
def add_store(store_name: str):
    # Check for auth etc

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


@store.post("/remove_store")
def remove_store(store_name: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@store.post("/store/add_package")
def add_package_to_store(store_name: str, package_name: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@store.post("/store/remove_package")
def remove_package_from_store(store_name: str, package_name: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@store.get("/store/check_package_exists")
def check_package_exists(store_name: str, package_name: str):
    # return {"package_exists": True}
    raise HTTPException(status_code=500, detail="Not implemented")


@store.get("/store/get_difference_paths")
def get_difference_of_paths(store_name1: str, store_name2: str):
    raise HTTPException(status_code=500, detail="Not implemented")


@store.get("/store/get_difference_paths")
def get_difference_of_package_closures(package1: str, package2: str):
    # ex: store1#bash,  store2#hello
    raise HTTPException(status_code=500, detail="Not implemented")
