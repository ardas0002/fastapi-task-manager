from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import User
from .schemas import UserCreate, UserLogin, Token, UserResponse
from .schemas import UserCreate, UserLogin, Token, UserResponse
from .service import hash_password, verify_password, create_access_token
from .dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
        ).first()
    
    if existing_user:
        raise HTTPException(status_code=400,
                            detail="Email already registered")
    
    user = User(email=user_data.email,
                username=user_data.username,
                password_hash=hash_password(user_data.password))
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, session: Session = Depends(get_session)):

    user = session.exec(
        select(User).where(User.email == credentials.email)
    ).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
      
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is disabled"
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return Token(access_token=access_token)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

