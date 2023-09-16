"""Создание таблиц и подключение базы данных + создание суперпользователя"""
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from users.hash import Hash
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
import databases

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

database = databases.Database(DATABASE_URL)

metadata = MetaData()

db_users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("is_admin", Boolean, default=False),
    Column("is_moderator", Boolean, default=False),
    Column("username", String, nullable=False, unique=True),
    Column("email", String, default=None, unique=True),
    Column("hashed_password", String, nullable=False, default=None),
    Column("friends", ARRAY(Integer), default=[]),
    Column("created_at", DateTime, nullable=False, default=datetime.now()),
)

db_content = Table(
    "content",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("link_to_storage", String, nullable=False, unique=True),
    Column("is_private", Boolean, default=False),
    Column("counter", Integer, nullable=False, default=1),
    Column("updated_at", DateTime, nullable=False, default=datetime.now()),
    Column("created_at", DateTime, nullable=False, default=datetime.now()),
)


db_tags = Table(
    "tags",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tag", String, nullable=False, unique=True),
)

db_useres_content = Table(
    "users_content",
    metadata,
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("content_id", Integer, ForeignKey("content.id"), nullable=False),
)


db_content_tags = Table(
    "content_tags",
    metadata,
    Column("tags_id", Integer, ForeignKey("tags.id"), nullable=False),
    Column("content_id", Integer, ForeignKey("content.id"), nullable=False),
)



metadata.create_all(engine)

s = db_users.select().where(db_users.c.username == "admin")
conn = engine.connect()
result = conn.execute(s).fetchall()
if len(result) == 0:
    ins = db_users.insert().values(username="admin",
                                   hashed_password=Hash().get_password_hash("admin"),
                                    is_admin=True, is_moderator = True, email="email",
                                    friends=[], created_at=datetime.now())
    conn = engine.connect()
    result = conn.execute(ins)