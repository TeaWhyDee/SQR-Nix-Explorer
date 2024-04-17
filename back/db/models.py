from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(unique=True)


class UserWithID(UserBase):
    id: int | None = Field(default=None, primary_key=True)


class User(UserWithID, table=True):
    password_hash: str


class UserStore(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field(unique=True)

    user_id: int | None = Field(default=None, foreign_key="user.id")
