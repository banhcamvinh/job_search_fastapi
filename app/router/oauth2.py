from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,SecurityScopes
from router import my_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    # scopes={
    #     "0": "User", 
    #     "1": "Admin"
    # }    
)

def get_current_user(security_scopes: SecurityScopes,token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )



    return my_token.verify_token(security_scopes,token,credentials_exception)
