from typing import List

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session

from src.types import CategoryDetail
from src.dependencies import get_db_session
from src.datebase import Category

router = APIRouter(
    prefix='/categories',
    default_response_class=ORJSONResponse,
)

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=List[CategoryDetail]
)
async def get_all_categories(session: Session = get_db_session):
    categories = session.query(Category).order_by(Category.id)
    return [CategoryDetail.model_validate(category, from_attributes=True) for category in categories]

