from fastapi import HTTPException, status, Depends
from users.models import UserIn, TokenData, User
from database_handler import database, db_users
from users.hash import Hash
from fastapi.security import OAuth2PasswordRequestForm
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from datetime import timedelta, datetime
from typing import Union, Annotated
from jose import JWTError, jwt


class UserServices:
    async def user_token_registration(self, user: UserIn):
      await self.check_unique(user)
      ins = dict(user)
      ins["created_at"] = datetime.now()
      ins["is_admin"] = False
      ins["is_moderator"] = False
      ins['friends'] = []
      ins['hashed_password'] = Hash().get_password_hash(user.password)
      del ins['password']
      query = db_users.insert().values(ins)
      last_record_id = await database.execute(query)
      return {**ins, "id": last_record_id}
  

    async def check_unique(self, current_user : UserIn):
      query = db_users.select().where(db_users.c.username == current_user.username)
      res = await database.fetch_one(query)
      if res != None:
          raise HTTPException(status_code=400,
                              detail="User with that email already exists")
      return res


    async def read_users(self, current_user: User, skip, limit,
                          user_id):
      if not current_user.is_admin and not current_user.is_moderator:
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="Not enough permissions"
          )
      sql_user_id = ''
      if user_id != None:
          sql_user_id = f"where id = {user_id}"
      query = f"SELECT * FROM users {sql_user_id} order by id OFFSET {skip} LIMIT {limit}"
      result = await database.fetch_all(query)
      return result


    async def delete_user(self, id, current_user: User):
      if (not current_user.is_admin and not current_user.is_moderator or
          current_user.id != id):
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="Not enough permissions"
          )
      query = f"DELETE FROM users WHERE id = {id}"
      await database.execute(query)
      return 200


    async def update_user(self, id, user: User, current_user : User):
      if not current_user.is_admin:
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="Not enough permissions"
          )
      query = f"SELECT * FROM users WHERE id = {id}"
      result = await database.fetch_one(query)
      if result == None:
        raise HTTPException(status_code=404, detail="User not found to update")
      to_update = dict(result)
      for k, v in user.dict().items():
        if v != None:
          to_update[k] = v
      query = db_users.update().where(db_users.c.id == to_update["id"]).values(to_update)
      await database.execute(query)
      return {**to_update}


    async def login_for_access_token(self,
      form_data : OAuth2PasswordRequestForm):
      user = await authenticate_user(form_data.username, form_data.password)
      if not user:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Incorrect username or password",
              headers={"WWW-Authenticate": "Bearer"},
          )
      access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      access_token = create_access_token(
          data={"sub": user.username}, expires_delta=access_token_expires
      )
      return {"access_token": access_token, "token_type": "bearer"}
 
async def get_current_user(token: Annotated[str, Depends(Hash().oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_user(username: str):
    query = f"SELECT * FROM users WHERE username = \'{username}\'"
    result = await database.fetch_one(query)
    if result == None:
       raise HTTPException(status_code=404, detail="Wrong username")
    temp = dict(result)
    return User(**temp)


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not Hash().verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
