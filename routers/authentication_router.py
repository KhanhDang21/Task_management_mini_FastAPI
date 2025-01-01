from fastapi import Depends, APIRouter, Depends, status, HTTPException
from config import authentication
from config.authentication import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from config.authentication import hash_password, verify_password
from config.database import user_collection
from models.user_model import User
from schemas.user_schema import user_serializer
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post('/register')
def register(user: User):
    new_user = {
        'username': user.username,
        'email': user.email,
        'password': hash_password(user.password),
        'role': user.role,
    }

    existing_user = user_collection.find_one({'email': user.email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail="Email already registered",
        )

    _id = user_collection.insert_one(new_user)
    new_user = user_collection.find_one({'_id': _id.inserted_id})
    return {
        'status': status.HTTP_200_OK,
        'data': user_serializer(new_user),
    }


@router.post('/login')
def login(user: OAuth2PasswordRequestForm = Depends()):
    this_user = user_collection.find_one({'username': user.username})
    if not this_user or not verify_password(user.password, this_user['password']):
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={'sub': this_user['email'], 'role': this_user['role'], 'user_id': str(this_user['_id'])},
        expires_delta=access_token_expires
    )
    return {
        'access_token': access_token,
        'token_type': 'Bearer',
    }
