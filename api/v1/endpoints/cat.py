from fastapi import APIRouter, Depends, status
from services.CatServices import CatService
from schema.cat import CatGet, CatCreate, CatUpdate
from api.deps import get_current_user_id

router = APIRouter(
    prefix="/cat",
)


@router.get("/{id}", response_model=CatGet, status_code=status.HTTP_200_OK)
def get_cat(id: int, catService: CatService = Depends()):
    return catService.get(id)


@router.post("", response_model=CatGet, status_code=status.HTTP_201_CREATED)
def create_cat(
    cat_body: CatCreate,
    catService: CatService = Depends(),
    current_user_id: str = Depends(get_current_user_id),
):
    return catService.create(cat_body, current_user_id)


@router.put("/{id}", response_model=CatGet, status_code=status.HTTP_200_OK)
def update_cat(
    id: int,
    cat_body: CatUpdate,
    catService: CatService = Depends(),
    current_user_id: str = Depends(get_current_user_id),
):

    return catService.update(id, cat_body, current_user_id)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_cat(
    id: int,
    catService: CatService = Depends(),
    current_user_id: str = Depends(get_current_user_id),
):
    catService.delete(id, current_user_id)
    return {"detail": "삭제되었습니다."}
