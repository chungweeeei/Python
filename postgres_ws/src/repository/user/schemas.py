from pydantic import (
    BaseModel,
    Field
)


class user(BaseModel):

    # Field aliases
    # for validation and serialization
    email: str = Field(...,
                       example="test@gmail.com",
                       description="user email")
    password: str = Field(...,
                          example="123",
                          description="user password")
