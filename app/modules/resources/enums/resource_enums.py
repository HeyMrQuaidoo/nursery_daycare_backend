import enum


class MediaType(enum.Enum):
    image = "image"
    video = "video"
    audio = "audio"
    document = "document"
    other = "other"
