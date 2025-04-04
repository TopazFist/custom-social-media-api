from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import schemas, database, models, oath2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oath2.get_current_user),
):
    # check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # check if user has already voted
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already voted"
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted"}
