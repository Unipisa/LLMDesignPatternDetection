from abc import ABC, abstractmethod
from enum import Enum


class AudioFormat(Enum):
    MP3 = "mp3"
    WAV = "wav"


class AudioDecoder(ABC):
    @abstractmethod
    def decode_stream(self) -> str:
        pass


class MP3Decoder(AudioDecoder):
    def decode_stream(self) -> str:
        return "Decoding MP3 frames using Fraunhofer algorithms."


class WAVDecoder(AudioDecoder):
    def decode_stream(self) -> str:
        return "Decoding raw PCM audio from WAV headers."


class MediaStreamingService(ABC):
    def __init__(self, audio: AudioFormat | None = None):
        self.audio_format = audio or self._default_audio_format()

    @abstractmethod
    def _default_audio_format(self) -> AudioFormat:
        pass

    @abstractmethod
    def create_decoder(self) -> AudioDecoder:
        pass

    def play_track(self, track_name: str) -> str | None:
        print(f"MediaService: Buffering {track_name} into memory...")
        decoder = self.create_decoder()
        audio_output = decoder.decode_stream()
        return f"Playing: {audio_output}"


class MP3StreamingService(MediaStreamingService):
    def _default_audio_format(self) -> AudioFormat:
        return AudioFormat.MP3

    def create_decoder(self) -> AudioDecoder:
        return MP3Decoder()


class WAVStreamingService(MediaStreamingService):
    def _default_audio_format(self) -> AudioFormat:
        return AudioFormat.WAV

    def create_decoder(self) -> AudioDecoder:
        return WAVDecoder()