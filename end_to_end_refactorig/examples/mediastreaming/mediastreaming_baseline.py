from enum import Enum

class AudioFormat(Enum):
    MP3 = "mp3"
    WAV = "wav"


class MediaStreamingService:
    def __init__(self, audio: AudioFormat):
        self.audio_format = audio

    def play_track(self, track_name: str) -> str | None:
        print(f"MediaService: Buffering {track_name} into memory...")

        if self.audio_format == AudioFormat.MP3:
            audio_output = "Decoding MP3 frames using Fraunhofer algorithms."
        elif self.audio_format == AudioFormat.WAV:
            audio_output = "Decoding raw PCM audio from WAV headers."
        else:
            raise ValueError(f"Unsupported audio format: {self.audio_format}")

        return f"Playing: {audio_output}"