from fastapi import Header, HTTPException

def validate_api_key(api_key: str = Header(...)):
    if not api_key:
        print("Missing API_KEY.")
        raise HTTPException(status_code=400, detail="Missing API_KEY.")
    return api_key



def validate_kernel_id(kernel_id: str = Header(...)):
    if not kernel_id:
        print("Missing KERNEL_ID.")
        raise HTTPException(status_code=400, detail="Missing KERNEL_ID.")
    return kernel_id