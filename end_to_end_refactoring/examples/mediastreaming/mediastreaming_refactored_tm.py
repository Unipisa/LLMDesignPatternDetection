from abc import ABC, abstractmethod

# Participant: AbstractClass
# Defines the skeleton of the streaming algorithm and declares the variable decoding step.
class StreamingService(ABC):

    # Common step shared by all concrete streaming services.
    def start_streaming(self, track_name: str):
        print(f"MediaService: Buffering {track_name} into memory...")

    # Primitive operation: subclasses provide the format-specific decoding behaviour.
    @abstractmethod
    def decode_stream(self):
        pass

    # Common step shared by all concrete streaming services.
    def start_playing(self, audio_output: str) -> str:
        return f"Playing: {audio_output}"

    def play_track(self, track_name: str) -> str:
        self.start_streaming(track_name)
        audio_output = self.decode_stream()
        return self.start_playing(audio_output)


# Participant: ConcreteClass
# Implements the primitive operation for MP3 audio streams.
class MP3StreamingService(StreamingService):
    def decode_stream(self):
        return "Decoding MP3 frames using Fraunhofer algorithms."

# Participant: ConcreteClass
# Implements the primitive operation for WAV audio streams.
class WAVStreamingService(StreamingService):
    def decode_stream(self):
        return "Decoding raw PCM audio from WAV headers."