import pydantic


class Model(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)
