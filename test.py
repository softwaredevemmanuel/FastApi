from fastapi import FastAPI, HTTPException, Body
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize FastAPI app
app = FastAPI()

# Define SQLAlchemy engine and base
DATABASE_URL = "postgresql://postgres:root@localhost:5432/marketz"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define Profile and User classes
class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Define endpoint for POST request
@app.post("/register")
async def create_user_profile(payload :dict = Body(...)):
    # Create new Profile instance
    print(payload['first_name'])
    new_profile = Profile(first_name=payload['first_name'], last_name=payload['last_name'], phone_number=payload['phone_number'])
    
    # Create new User instance
    new_user = User(email=payload['email'], password=payload['password'])
    
    # Add instances to session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    db.add(new_profile)
    db.add(new_user)
    db.commit()
    db.close()
    
    return {"message": "User and Profile created successfully"}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
