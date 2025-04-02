from .. import schemas, models, utils
from fastapi import Depends, Response, status, HTTPException, APIRouter
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash password
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    delete_user = db.query(models.User).filter(models.User.id == id).delete()
    db.commit()

    if not delete_user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.UserOut)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):

    query_user = db.query(models.User).filter(models.User.id == id)
    update_user = query_user.first()

    if not update_user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    query_user.update(user.model_dump(), synchronize_session=False)

    db.commit()

    return query_user.first()
