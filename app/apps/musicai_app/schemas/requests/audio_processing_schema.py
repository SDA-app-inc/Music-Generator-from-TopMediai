from pydantic import BaseModel


class GenerateTextRequestSchema(BaseModel):
    text: str


class GenerateTextToSpeechRequestSchema(GenerateTextRequestSchema):
    voice_id: str | None = None


class SoundGenerationRequestSchema(GenerateTextRequestSchema):
    pass


class SpeechSynthesisPayloadSchema(BaseModel):
    text: str
    speaker: str
    emotion: str


class SongGenerationPayloadSchema(BaseModel):
    lyrics: str
    instrumental: str | None = None
