from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from .schemas import UserSchema, RegisterSchema, UpdateProfileSchema, ErrorSchema
from .models import User

router = Router()

@router.post("/register", response={201: UserSchema, 400: ErrorSchema})
def register(request, data: RegisterSchema):
    if User.objects.filter(username=data.username).exists():
        return 400, {"message": "Username already exists"}
    if User.objects.filter(email=data.email).exists():
        return 400, {"message": "Email already exists"}
    
    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        role=data.role
    )
    return 201, user

@router.get("/me", auth=JWTAuth(), response=UserSchema)
def get_me(request):
    return request.auth

@router.put("/me", auth=JWTAuth(), response=UserSchema)
def update_me(request, data: UpdateProfileSchema):
    user = request.auth
    for attr, value in data.dict(exclude_none=True).items():
        setattr(user, attr, value)
    user.save()
    return user
