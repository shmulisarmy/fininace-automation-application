from fastapi import HTTPException
from fastapi import Request
import json
from encryption import decrypt

def get_auth_details(request: Request) -> str: 
    cookies = request.cookies
    access_token = cookies.get("access_token")
    print(f'{access_token = }')
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Not logged in")
    

    print(f'{access_token = }')
    
    decoded = decrypt(access_token)
    auth_details = json.loads(decoded)
    print(f'{auth_details = }')
    
    return auth_details['sub']
