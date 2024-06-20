from fastapi import Header, HTTPException
from .secret import APIKeyManager

api_key_manager = APIKeyManager()  


def validate_api_key(api_key: str = Header(None)):
    if not api_key:
        print("Missing API_KEY.")
        raise HTTPException(status_code=400, detail="Missing API_KEY.")
    if not api_key_manager.validate_api_key(api_key):
        print("Invalid API_KEY.")
        raise HTTPException(status_code=400, detail="Invalid API_KEY.")
    return api_key



def validate_kernel_id(kernel_id: str = Header(None)):
    if not kernel_id:
        print("Missing KERNEL_ID.")
        raise HTTPException(status_code=400, detail="Missing KERNEL_ID.")
    return kernel_id