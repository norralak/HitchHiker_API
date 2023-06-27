from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import schemaz, database, model, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemaz.Vote, db: Session = Depends(database.get_db), getCurrentUser: int = Depends(oauth2.getCurrentUser)):

    query = db.query(model.Votes).filter(model.Votes.user_id == getCurrentUser.id, model.Votes.message_id == vote.message_id)

    if vote.upDown == 13:
        if query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {getCurrentUser.id} has already voted on message {vote.message_id}')
        
        else:
            if not db.query(model.Message).filter(model.Message.id == vote.message_id).first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Message {vote.message_id} not found.')
            new_vote = model.Votes(user_id=getCurrentUser.id, message_id=vote.message_id)
            db.add(new_vote)
            db.commit()
            return {"Message":f"Voted for message {vote.message_id}"}
    
    else:
        if not query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Message {vote.message_id} vote not found.')

        query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Unvoted"}


