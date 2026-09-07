from pydantic import BaseModel, Field


class Story(BaseModel):
    title: str | None = None


class ComicMetadata(BaseModel):
    series: str | None = None
    issue: str | None = None

    title: str | None = None
    stories: list[Story] = Field(default_factory=list)

    year: int | None = None
    month: int | None = None
    day: int | None = None

    volume: int | None = None
    count: int | None = None

    publisher: str | None = None
    imprint: str | None = None

    writers: list[str] = Field(default_factory=list)
    pencillers: list[str] = Field(default_factory=list)
    inkers: list[str] = Field(default_factory=list)
    colorists: list[str] = Field(default_factory=list)

    genres: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

    summary: str | None = None

    page_count: int | None = None
    format: str | None = None
    scan_information: str | None = None

    extension: str | None = None
