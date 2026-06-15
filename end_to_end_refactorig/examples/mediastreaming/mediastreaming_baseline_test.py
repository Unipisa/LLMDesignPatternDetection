import unittest
from unittest.mock import patch
import os
import sys
import importlib.util

# Load the module dynamically since it starts with a number
module_name = 'mediastreaming_baseline'
module_path = os.path.join(os.path.dirname(__file__), f'{module_name}.py')

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

AudioDecoder = module.AudioFormat
MediaStreamingService = module.MediaStreamingService


class MP3Decoder:
    def decode_stream(self) -> str:
        with patch('builtins.print'):
            result = MediaStreamingService(AudioDecoder.MP3).play_track("")
        return result.replace("Playing: ", "")


class WAVDecoder:
    def decode_stream(self) -> str:
        with patch('builtins.print'):
            result = MediaStreamingService(AudioDecoder.WAV).play_track("")
        return result.replace("Playing: ", "")


class MP3StreamingService:
    def create_decoder(self) -> MP3Decoder:
        return MP3Decoder()

    def play_track(self, track_name: str) -> str:
        return MediaStreamingService(AudioDecoder.MP3).play_track(track_name)


class WAVStreamingService:
    def create_decoder(self) -> WAVDecoder:
        return WAVDecoder()

    def play_track(self, track_name: str) -> str:
        return MediaStreamingService(AudioDecoder.WAV).play_track(track_name)


class TestAudioDecoders(unittest.TestCase):

    def test_mp3_decoder_decode_stream(self):
        decoder = MP3Decoder()
        result = decoder.decode_stream()
        self.assertEqual(result, "Decoding MP3 frames using Fraunhofer algorithms.")

    def test_wav_decoder_decode_stream(self):
        decoder = WAVDecoder()
        result = decoder.decode_stream()
        self.assertEqual(result, "Decoding raw PCM audio from WAV headers.")


class TestMediaStreamingServices(unittest.TestCase):

    def setUp(self):
        patcher = patch('builtins.print')
        self.mock_print = patcher.start()
        self.addCleanup(patcher.stop)

    def test_mp3_streaming_service_create_decoder(self):
        service = MP3StreamingService()
        decoder = service.create_decoder()
        self.assertIsInstance(decoder, MP3Decoder)

    def test_wav_streaming_service_create_decoder(self):
        service = WAVStreamingService()
        decoder = service.create_decoder()
        self.assertIsInstance(decoder, WAVDecoder)

    def test_mp3_streaming_service_play_track(self):
        service = MP3StreamingService()
        track_name = "awesome_song.mp3"
        result = service.play_track(track_name)

        self.mock_print.assert_called_once_with(f"MediaService: Buffering {track_name} into memory...")
        self.assertEqual(result, "Playing: Decoding MP3 frames using Fraunhofer algorithms.")

    def test_wav_streaming_service_play_track(self):
        service = WAVStreamingService()
        track_name = "lossless_song.wav"
        result = service.play_track(track_name)

        self.mock_print.assert_called_once_with(f"MediaService: Buffering {track_name} into memory...")
        self.assertEqual(result, "Playing: Decoding raw PCM audio from WAV headers.")


if __name__ == '__main__':
    unittest.main()