from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserRegister(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("A valid email address is required")
        return value


class UserLogin(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1, max_length=128)


class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    ingredients: str = Field(min_length=1)
    steps: str = Field(min_length=1)


class RecipeUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    ingredients: str = Field(min_length=1)
    steps: str = Field(min_length=1)


class RecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    ingredients: str
    steps: str
