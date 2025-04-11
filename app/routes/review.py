from fastapi import APIRouter, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.schemas.review import ReviewCreate, ReviewOut, ReviewUpdate
from app.controller import review as crud
from typing import List

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=str)
async def create_review(review: ReviewCreate):
    return await crud.create_review(review.dict())

@router.get("/", response_model=List[ReviewOut])
async def get_reviews():
    return await crud.get_all_reviews()

@router.get("/{review_id}", response_model=ReviewOut)
async def get_review(review_id: str):
    review = await crud.get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review no encontrada")
    return review

@router.put("/{review_id}")
async def update_review(review_id: str, review: ReviewUpdate):
    modified = await crud.update_review(review_id, review.dict(exclude_unset=True))
    if not modified:
        raise HTTPException(status_code=404, detail="Review no encontrada o sin cambios")
    return {"message": "Actualizado correctamente"}

@router.delete("/{review_id}")
async def delete_review(review_id: str):
    deleted = await crud.delete_review(review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review no encontrada")
    return {"message": "Eliminada correctamente"}
