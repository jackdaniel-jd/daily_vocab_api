from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Word, PracticeSession
from app.schemas import ValidateSentenceRequest, ValidateSentenceResponse
from app.utils import mock_ai_validation

router = APIRouter()


@router.post("/validate-sentence", response_model=ValidateSentenceResponse)
def validate_sentence(
    request: ValidateSentenceRequest,
    db: Session = Depends(get_db)
):
    """
    Receive user sentence and validate it (mock AI)
    Save results to database
    """
 # Get word data
    word = db.query(Word).filter(Word.id == request.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Mock AI validation
    result = mock_ai_validation(word.word, request.sentence, word.difficulty_level)
    
    # Save to database
    practice_session = PracticeSession(
        word_id=request.word_id,
        user_sentence=request.sentence,
        score=result["score"],
        feedback=result["suggestion"],
        corrected_sentence=result["corrected_sentence"]
    )
    db.add(practice_session)
    db.commit()
    
    return ValidateSentenceResponse(**result)