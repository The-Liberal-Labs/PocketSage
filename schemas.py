"""
Pydantic models for PocketSage API request/response validation.
"""

from datetime import datetime
from typing import Annotated, Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field


def convert_objectid_to_str(v: Any) -> Optional[str]:
    """Convert MongoDB ObjectId to string."""
    if v is None:
        return None
    return str(v)


# Custom type that converts ObjectId to str
PyObjectId = Annotated[Optional[str], BeforeValidator(convert_objectid_to_str)]

# Generic type for StandardResponse
T = TypeVar("T")


# =============================================================================
# Response Wrapper
# =============================================================================


class StandardResponse(BaseModel, Generic[T]):
    """Generic wrapper for all API responses."""

    status: bool = True
    data: Optional[T] = None
    message: str = ""


class SimpleMessageResponse(BaseModel):
    """Simple message-only response."""

    message: str


# =============================================================================
# Authentication & User Models
# =============================================================================


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: EmailStr
    username: str
    full_name: str


class UserCreate(UserBase):
    """User registration request model."""

    password: str


class UserInDB(UserBase):
    """User model as stored in database (includes hashed password)."""

    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(default=None, alias="_id")
    hashed_password: str
    age: Optional[int] = None
    gender: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    allergies: Optional[List[str]] = None
    previous_issues: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None


class UserProfile(BaseModel):
    """User profile response model (excludes sensitive data)."""

    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(default=None, alias="_id")
    email: EmailStr
    username: str
    full_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    allergies: Optional[List[str]] = None
    previous_issues: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None


class UserProfileUpdate(BaseModel):
    """User profile update request model."""

    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    weight_kg: Optional[float] = None
    height_cm: Optional[float] = None
    allergies: Optional[List[str]] = None
    previous_issues: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None


class Token(BaseModel):
    """JWT token response model."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """JWT token payload data."""

    username: str


# =============================================================================
# Chat Models
# =============================================================================


class SourceCitation(BaseModel):
    """Citation source for AI responses with web grounding."""

    url: str
    title: str
    index: int


class ChatMessage(BaseModel):
    """Individual message in chat history."""

    role: str  # "user" or "assistant"
    content: str
    turn_number: Optional[int] = None
    citations: Optional[List[SourceCitation]] = None


class ChatRequest(BaseModel):
    """Request to send a message in chat."""

    prompt: str
    chat_id: Optional[str] = None  # None for new chat session


class ChatTurnResponse(BaseModel):
    """Response for a single chat turn."""

    chat_id: str
    ai_response: str
    turn_number: int
    citations: List[SourceCitation] = []


class ChatSession(BaseModel):
    """Chat session with full history."""

    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(default=None, alias="_id")
    user_id: str
    history: List[ChatMessage] = []
    chat_name: str
    created_at: datetime
    updated_at: datetime


class RenameChatRequest(BaseModel):
    """Request to rename a chat session."""

    new_name: str


# =============================================================================
# Appointment Models
# =============================================================================


class AppointmentCreate(BaseModel):
    """Request to create a new appointment."""

    doctor_name: str
    specialization: str
    appointment_time: datetime


class AppointmentUpdate(BaseModel):
    """Request to update an existing appointment."""

    doctor_name: Optional[str] = None
    specialization: Optional[str] = None
    appointment_time: Optional[datetime] = None


class AppointmentInDB(BaseModel):
    """Appointment model as stored in database."""

    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(default=None, alias="_id")
    user_id: str
    doctor_name: str
    specialization: str
    appointment_time: datetime
    transcript: Optional[str] = None
    summary: Optional[str] = None
    structured_summary: Optional[dict] = None
    audio_path: Optional[str] = None
    processed_at: Optional[datetime] = None


class TranscriptionResponse(BaseModel):
    """Response after audio transcription and processing."""

    appointment_id: str
    transcript: str
    summary: str
    structured_summary: dict


# =============================================================================
# Hospital/Location Models
# =============================================================================


class LocationRequest(BaseModel):
    """Request to find nearby hospitals/facilities."""

    latitude: float
    longitude: float


class Hospital(BaseModel):
    """Hospital or medical facility information."""

    name: str
    type: str  # e.g., "Hospital", "Clinic", "Pharmacy"
    latitude: float
    longitude: float
    phone: Optional[str] = None
    address: Optional[str] = None
    google_maps_url: Optional[str] = None
