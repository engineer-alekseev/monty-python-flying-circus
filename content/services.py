from fastapi import HTTPException
from users.models import User
from database_handler import (database, db_content,
                              db_useres_content, db_tags,
                              db_content_tags)
from content.models import ContentIn
from datetime import datetime


async def post_content(current_user: User, content: ContentIn, tag):
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

        if tag != None:
            query = f"SELECT * FROM tags where tag = \'{tag}\'"
            tag_res = await database.fetch_one(query)
            if tag_res == None:
                query = db_tags.insert().values(tag=tag)
                tag_id = await database.execute(query)
                query = db_content_tags.insert().values(tags_id=tag_id,
                                                        content_id=last_record_id)
                await database.execute(query)
            else:
                query = db_content_tags.insert().values(tags_id=tag_res.id,
                                                        content_id=last_record_id)
                await database.execute(query)
        
        return {**ins, "id": last_record_id}
    else:
        query = db_useres_content.select().where(
            db_useres_content.c.user_id == current_user.id,
            db_useres_content.c.content_id == dict(res)['id'])
        check_self_lib = await database.fetch_one(query)
        if check_self_lib != None:
            raise HTTPException(status_code=403,
                                detail="Content already in your list")

        ins = dict(res)
        ins["updated_at"] = datetime.now()
        ins['counter'] = ins['counter'] + 1
        query = db_content.update().values(ins).where(
            db_content.c.link_to_storage == content.link_to_storage)
        await database.execute(query)
        query = db_useres_content.insert().values(
            user_id=current_user.id, content_id=ins['id'])
        await database.execute(query)

    return ins


async def delete_content(current_user: User, id: int):
    query = db_content.select().where(db_content.c.id == id)
    content_res = await database.fetch_one(query)
    if content_res == None:
        raise HTTPException(status_code=404,
                            detail="Content not found")
    
    if not current_user.is_admin and not current_user.is_moderator:
        # Удаляю связь картинки с текущим пользователем
        query = db_useres_content.delete().where(
            db_useres_content.c.user_id == current_user.id,
            db_useres_content.c.content_id == id
        )
        await database.execute(query)
        # Если это была последняя подписка на картинку, удаляем ее, иначе уменьшаем счетчик на 1
        if content_res['counter'] == 1:
            query = db_content.delete().where(
                db_content.c.id == id
            )
            await database.execute(query)
            query = db_content_tags.delete().where(content_id=id)
            await database.execute(query)
        else:
            query = db_content.update().values(counter=content_res['counter'] - 1).where(
                db_content.c.id == id
            )
            await database.execute(query)

    else:
        # Если админ или модератор удаляем все связи с этой картинкой и ее саму
        query = db_useres_content.delete().where(
            db_useres_content.c.content_id == id
        )
        await database.execute(query)

        query = db_content.delete().where(
            db_content.c.id == id
        )
        await database.execute(query)

        query = db_content_tags.delete().where(content_id=id)
        await database.execute(query)

    return 200


async def get_content(current_user : User, skip, limit, order_by,
                      order_desc, filter_tag):
    order_by_desc = 'DESC' if order_desc else 'ASC'
    sql_private, sql_and = '', ''
    sql_where = ''
    sql_filter_tag = ''
    if filter_tag != None:
        sql_where = "WHERE"
        sql_filter_tag = f"tag = '{filter_tag}'"

    if not current_user.is_admin and not current_user.is_moderator:
        if filter_tag != None:
            sql_and = 'AND'
        sql_private = 'is_private = false'
        sql_where = "WHERE"
    query = (f"SELECT * FROM content JOIN content_tags ON content.id = content_id "
             "JOIN tags ON content_tags.tags_id = tags.id "
             f"{sql_where} {sql_private} {sql_and} {sql_filter_tag} order by "
             f"{order_by} {order_by_desc} OFFSET {skip} LIMIT {limit}")
    result = await database.fetch_all(query)

    return_list = []
    for res in result:
        return_list.append(res)

    return return_list


async def get_own_content(current_user : User, skip, limit, order_by,
                      order_desc, filter_tag):
    order_by_desc = 'DESC' if order_desc else 'ASC'
    sql_and, sql_filter_tag = '', ''
    if filter_tag != None:
        sql_and = "AND"
        sql_filter_tag = f"tag = '{filter_tag}'"

    
    query = (f"SELECT * FROM users_content "
             "JOIN content ON id = users_content.content_id "
             "JOIN content_tags ON content.id = content_tags.content_id "
             "JOIN tags ON content_tags.tags_id = tags.id "
             f"WHERE user_id = {current_user.id} {sql_and} {sql_filter_tag} order by "
             f"{order_by} {order_by_desc} OFFSET {skip} LIMIT {limit}")
    result = await database.fetch_all(query)

    return_list = []
    for res in result:
        return_list.append(res)

    return return_list
