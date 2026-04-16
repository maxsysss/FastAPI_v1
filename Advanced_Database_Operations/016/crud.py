from sqlalchemy.orm import Session, selectinload
from sqlalchemy.future import select
from sqlalchemy import func
import models
import schemas

def create_user_with_items(db: Session, user: schemas.UserCreate, item_titles: list[str]):
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    db.flush()  # Get the user.id before committing

    items = [models.Item(title=title, owner_id=new_user.id) for title in item_titles]
    db.add_all(items)
    db.commit()
    db.refresh(new_user)
    return new_user

def search_items(db: Session, keyword: str):
    stmt = select(models.Item).where(models.Item.title.ilike(f"%{keyword}%"))
    return db.execute(stmt).scalars().all()

def get_user_item_counts(db: Session):
    stmt = (
        select(models.User.name, func.count(models.Item.id).label("item_count"))
        .join(models.User.items)
        .group_by(models.User.id)
    )
    result = db.execute(stmt).all()
    # Convert to a list of dictionaries for JSON serialization
    return [{"name": name, "item_count": count} for name, count in result]

def get_users_with_items(db: Session):
    stmt = select(models.User).options(
        selectinload(models.User.items)
    )
    return db.execute(stmt).scalars().all()