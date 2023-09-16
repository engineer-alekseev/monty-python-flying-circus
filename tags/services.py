from fastapi import HTTPException, status
from users.models import User
from database_handler import database, db_tags


async def post_tag(tag):
    query = db_tags.select().where(db_tags.c.tag == tag)
    res = await database.fetch_one(query)
    if res == None:
        query = db_tags.insert().values(tag=tag)
        tag_id = await database.execute(query)
        return {"id" : tag_id, "tag" : tag}
    else:
        raise HTTPException(status_code=400,
                            detail="Tag already exists")
    
async def get_tags(skip, limit, order_by, order_desc):
    order_desc = "DESC" if order_desc else "ASC"
    sql_order_by = f"ORDER BY {order_by} {order_desc}"
    query = f"SELECT * FROM tags {sql_order_by} OFFSET {skip} LIMIT {limit}"
    res = await database.fetch_all(query)
    return_list = []
    if res != None:
        for row in res:
            return_list.append(dict(row))
    return return_list

async def delete_tag(current_user: User, tag_id):
    if not current_user.is_admin and not current_user.is_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    query = f"DELETE FROM tags WHERE id = {tag_id}"
    await database.execute(query)
    return 200