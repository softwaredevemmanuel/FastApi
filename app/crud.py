from sqlalchemy.orm import Session
from model import Profile, User
from schemas import ProfileSchema, UserSchema
from sqlalchemy.exc import IntegrityError


# Get All profile data
def get_user(db:Session, skip:int=0, limit:int=100):
    return db.query(Profile).offset(skip).limit(limit).all()

# Get by ID profile data
def get_user_by_id(db:Session, user_id: int):
    return db.query(Profile).filter(Profile.id == user_id).first()


# Create profile data
# def create_profile(db:Session, profile:ProfileSchema):
#     _profile = Profile(firstName=profile.firstName, lastName=profile.lastName, email=profile.email, phoneNumber = profile.phoneNumber)
#     db.add(_profile)
#     db.commit()
#     db.refresh(_profile)
#     return _profile


def create_profile_and_user(db: Session, request_profile: ProfileSchema):
    print('hahahah')

    try:
        existing_profile = get_user_by_email(db, email=request_profile.email)
        if existing_profile:
            # User already exists with this email
            return None
        
        # Create profile
        _profile = Profile(
            first_name=request_profile.first_name,
            last_name=request_profile.last_name,
            email=request_profile.email,
            phone_number=request_profile.phone_number
        )

        db.add(_profile)
        db.flush()  # Ensure the profile is persisted to get its ID
        
        # Create user
        _user = User(
            email=request_user.email,
            password=request_user.password,  # Assuming 'password' is in UserSchema
        )
        db.add(_user)
        db.commit()
        
        return _profile  # Return the created profile
    except IntegrityError:
        # Handle any integrity errors here
        db.rollback()
        return None


# Remove profile data
def remove_profile(db:Session, profile_id:int):
    _profile = get_profile_by_id(db=db, profile_id=profile_id)
    db.delete(_profile)
    db.commit()



def update_profile(db: Session, profile_id: int, title: str, description: str):
    # Check if profile exists
    _profile = db.query(profile).filter(profile.id == profile_id).first()
    if not _profile:
        raise ValueError("profile not found")

    # Update profile attributes
    if title is not None:
        _profile.title = title
    if description is not None:
        _profile.description = description

    # Commit changes to the database
    try:
        db.commit()
        db.refresh(_profile)
        return _profile
    except Exception as e:
        # Rollback changes in case of error
        db.rollback()
        raise RuntimeError(f"Error updating profile: {str(e)}")



def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
