from abc import ABC, abstractmethod

class DecodingStrategy(ABC):
    @abstractmethod
    def decode_stream(self, track_name: str) -> str:
        pass

class MP3DecodingStrategy(DecodingStrategy):
    def decode_stream(self, track_name: str) -> str:
        return "Decoding MP3 frames using Fraunhofer algorithms."

class WavDecodingStrategy(DecodingStrategy):
    def decode_stream(self, track_name: str) -> str:
        return "Decoding raw PCM audio from WAV headers."

class MediaStreamingService:
    def __init__(self, decoding_strategy: DecodingStrategy):
        self.decoding_strategy = decoding_strategy

    def play_track(self, track_name: str) -> str:
        print(f"MediaService: Buffering {track_name} into memory...")
        audio_output = self.decoding_strategy.decode_stream(track_name)
        return f"Playing: {audio_output}"