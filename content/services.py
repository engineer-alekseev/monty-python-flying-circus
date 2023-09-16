from fastapi import HTTPException, status, Depends
from users.models import UserIn, TokenData, User
from database_handler import database, db_content, db_useres_content
from content.models import ContentIn
from datetime import timedelta, datetime


async def post_content(current_user: User, content: ContentIn):
    query = db_content.select().where(db_content.c.link_to_storage == content.link_to_storage)
    res = await database.fetch_one(query)
    if res == None:
        ins = dict(content)
        ins["created_at"] = datetime.now()
        ins['counter'] = 1
        ins['updated_at'] = datetime.now()

        query = db_content.insert().values(ins)
        last_record_id = await database.execute(query)

        query = db_useres_content.insert().values(
            user_id=current_user.id, content_id=last_record_id)
        await database.execute(query)
    else:
        query = db_useres_content.select().where(
            db_useres_content.c.user_id == current_user.id,
            db_useres_content.c.content_id == dict(res)['id'])
        check_self_lib = await database.fetch_one(query)
        if check_self_lib != None:
            raise HTTPException(status_code=403,
                                detail="Content already in your list")


        ins = {}
        ins["updated_at"] = datetime.now()
        ins['counter'] = dict(res)['counter'] + 1
        query = db_content.update().values(ins).where(
            db_content.c.link_to_storage == content.link_to_storage)
        last_record_id = await database.execute(query)

        query = db_useres_content.insert().values(
            user_id=current_user.id, content_id=last_record_id)
        await database.execute(query)

    return ins


# async def check_unique(content : ContentIn):
#     query = db_content.select().where(db_content.c.link_to_storage == content.link_to_storage)
#     res = await database.fetch_one(query)
#     if res == None:
#         return True
#     raise HTTPException(status_code=403,
#                         detail="User with that email already exists")


# async def read_users(self, current_user: User, skip, limit,
#                         user_id):
#     if not current_user.is_admin and not current_user.is_moderator:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not enough permissions"
#         )
#     sql_user_id = ''
#     if user_id != None:
#         sql_user_id = f"where id = {user_id}"
#     query = f"SELECT * FROM users {sql_user_id} order by id OFFSET {skip} LIMIT {limit}"
#     result = await database.fetch_all(query)
#     return result


# async def delete_user(self, id, current_user: User):
#     if (not current_user.is_admin and not current_user.is_moderator or
#         current_user.id != id):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not enough permissions"
#         )
#     query = f"DELETE FROM users WHERE id = {id}"
#     await database.execute(query)
#     return 200


# async def update_user(self, id, user: User, current_user : User):
#     if not current_user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not enough permissions"
#         )
#     query = f"SELECT * FROM users WHERE id = {id}"
#     result = await database.fetch_one(query)
#     if result == None:
#     raise HTTPException(status_code=404, detail="User not found to update")
#     to_update = dict(result)
#     for k, v in user.dict().items():
#     if v != None:
#         to_update[k] = v
#     query = db_users.update().where(db_users.c.id == to_update["id"]).values(to_update)
#     await database.execute(query)
#     return {**to_update}

 


