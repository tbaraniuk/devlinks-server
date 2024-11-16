from fastapi import APIRouter, Depends

from schemas.user import UserSchema
from schemas.link import GetLinksSchema, LinkCreateSchema
from auth.utils import get_current_user
from database import SessionDep
from models.link import Link

router = APIRouter(
    prefix='/links',
    tags=['links']
)


@router.post('/', response_model=GetLinksSchema)
def get_links(links: list[LinkCreateSchema], session: SessionDep, user: UserSchema = Depends(get_current_user)):
    """
    Add links for currently authenticated user
    """
    for link_data in links:
        link = Link(**link_data.model_dump(), owner_id=user.id)
        session.add(link)

    session.commit()
    session.refresh(user)

    return {'links': user.links}