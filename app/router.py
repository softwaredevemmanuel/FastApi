from fastapi import APIRouter, HTTPException, Body, Path, Depends, Query, status
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import RequestProfile, Response, ProfileSchema, EmailCheckRequest, RequestUser, UserSchema
import crud
from sqlalchemy.orm import sessionmaker

from model import Profile, User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# @router.post('/register')
# async def create( request_profile: RequestProfile,  db: Session = Depends(get_db)):
#     print('hahahah')

#     # print(request_profile.dict)
#     new_profile = crud.create_profile_and_user(
#         db,
#         request_profile=request_profile.profile_parameter,  # Pass the profile data
#     )


#     if new_profile:
#         # Profile created successfully

#         return Response(
#             code="200",
#             status="Ok",
#             message="Profile created successfully",
#             result=new_profile
#         ).dict(exclude_none=True)
#     else:
#         # User with this email already exists
#         return Response(
#             code="400",
#             status="Bad Request",
#             message="User with this email already exists",
#             result=None
#         ).dict(exclude_none=True)
    


# CREATE USER 1

# @router.post("/register")
# async def create_user_profile(request_profile: ProfileSchema, request_user: UserSchema, db: Session = Depends(get_db)):
#     # Check if profile with the provided email already exists
#     existing_profile = crud.get_user_by_email(db, email=request_profile.email)
#     if existing_profile:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile with this email already exists")
    
#     # If profile doesn't exist, proceed with creating both profile and user
#     new_profile = Profile(
#         first_name=request_profile.first_name,
#         last_name=request_profile.last_name,
#         email=request_profile.email,
#         phone_number=request_profile.phone_number
#     )

#     new_user = User(
#         email=request_user.email,
#         password=request_user.password,
#     )

#     # Add instances to session
#     db.add(new_profile)
#     db.add(new_user)
#     db.commit()
#     db.close()

#  # Remove the password field from request_user before returning
#     user_data = request_user.dict()
#     user_data.pop("password", None)

#     return {"success": True, "message": "Account created successfully", "data": {"user": user_data, "profile": request_profile}}

# CREATE USER 2

@router.post("/register")
async def create_user_profile(payload: dict = Body(...), db: Session = Depends(get_db)):
    try:
        # Check if profile with the provided email already exists
        existing_profile = crud.get_user_by_email(db, email=payload['email'])
        if existing_profile:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile with this email already exists")
        
        # If profile doesn't exist, proceed with creating both profile and user
        new_profile = Profile(
            first_name=payload['first_name'],
            last_name=payload['last_name'],
            email=payload['email'],
            phone_number=payload['phone_number']
        )

        new_user = User(
            email=payload['email'],
            password=payload['password'],
        )

        # Add instances to session
        db.add(new_profile)
        db.add(new_user)
        db.commit()

        # Refresh the profile instance to make sure it's properly bound to the session
        db.refresh(new_profile)

        # Create schema instances from the newly created profile and user objects
        profile_schema = ProfileSchema.from_orm(new_profile)
        user_schema = UserSchema.from_orm(new_user)

        # Return the profile and user schemas in the response
        return {"success": True, "message": "Account created successfully", "data": {"profile": profile_schema.dict(), "user": user_schema.dict()}}
    except Exception as e:
        # Rollback changes in case of error
        db.rollback()
        raise e
    finally:
        # Close the session
        db.close()


@router.get("/profile")
async def get(db:Session=Depends(get_db)):
    _profile = crud.get_profile(db, 0,100)
    return Response(code="200", status="Ok", message= "Success Fetch all data", result=_profile).dict(exclude_none=True)

@router.get("/{id}")
async def get_by_id(id: int, db: Session = Depends(get_db)):
    _profile = crud.get_profile_by_id(db, id)
    return Response(code="200", status="Ok", message="Success get data", result=_profile).dict(exclude_none=True)

@router.patch("/update")
async def update_profile(request: RequestProfile, db:Session = Depends(get_db)):
    _profile = crud.update_profile(db, profile_id = request.parameter.id, title = request.parameter.title, description=request.parameter.description)
    return Response(code="200", status="Ok", message="Success update data", result=_profile).dict(exclude_none=True)


@router.delete("/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    try:
        crud.remove_profile(db, profile_id=id)
        return Response(code="200", status="ok", message="success delete data", result="").dict(exclude_none=True)
    except Exception as e:
        # Log the error or handle it appropriately
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

from pydantic import BaseModel


# Using Post Method to veryfy email existence
@router.post("/check-email")
async def check_email(request_data: EmailCheckRequest = Body(...), db: Session = Depends(get_db)):
    profile = crud.get_user_by_email(db, request_data.email)
    if profile:
        return {"email_exists": True}
    else:
        return {"email_exists": False}


# Using Get method to verify email existence
@router.get("/check-email/{email}")
async def check_email(email: str, db: Session = Depends(get_db)):
    profile = crud.get_user_by_email(db, email)
    if profile:
        return {"email_exists": True}
    else:
        return {"email_exists": False}
