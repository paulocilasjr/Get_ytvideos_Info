from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class Video(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(alias="ID", ge=1)
    title: str = Field(alias="Title", min_length=1)
    url: HttpUrl = Field(alias="URL")


class VideoExport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    videos: list[Video] = Field(alias="Videos")
