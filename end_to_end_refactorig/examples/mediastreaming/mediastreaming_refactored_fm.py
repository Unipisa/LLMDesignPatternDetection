from abc import ABC, abstractmethod

# Participant: Product
class AudioDecoder(ABC):
    @abstractmethod
    def decode_stream(self) -> str:
        pass

# Participant: ConcreteProduct
class MP3Decoder(AudioDecoder):
    def decode_stream(self) -> str:
        return "Decoding MP3 frames using Fraunhofer algorithms."

# Participant: ConcreteProduct
class WAVDecoder(AudioDecoder):
    def decode_stream(self) -> str:
        return "Decoding raw PCM audio from WAV headers."

# Participant: Creator
class MediaStreamingService(ABC):
    # The Factory Method
    @abstractmethod
    def create_decoder(self) -> AudioDecoder:
        pass

    def play_track(self, track_name: str) -> str:
        print(f"MediaService: Buffering {track_name} into memory...")
        
        decoder = self.create_decoder()
        audio_output = decoder.decode_stream()
        
        return f"Playing: {audio_output}"

# Participant: ConcreteCreator
class MP3StreamingService(MediaStreamingService):
    def create_decoder(self) -> AudioDecoder:
        return MP3Decoder()

# Participant: ConcreteCreator
class WAVStreamingService(MediaStreamingService):
    def create_decoder(self) -> AudioDecoder:
        return WAVDecoder()