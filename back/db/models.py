from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password_hash: str


class UserStore(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str

    user_id: int | None = Field(default=None, foreign_key="user.id")
