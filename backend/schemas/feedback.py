from pydantic import BaseModel, ConfigDict, Field


class FeedbackCreate(BaseModel):
    user_id: int
    charging_station_id: int
    comments: str | None = None

    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")


class FeedbackUpdate(BaseModel):
    comments: str | None = None

    rating: int | None = Field(default=None, ge=1, le=5)


class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    charging_station_id: int
    comments: str | None
    rating: int

    model_config = ConfigDict(from_attributes=True)
