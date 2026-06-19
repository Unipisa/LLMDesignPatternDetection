import unittest
from unittest.mock import patch
import os
import sys
import importlib.util

# Load the module dynamically since it starts with a number
module_name = 'mediastreaming_refactored_str'
module_path = os.path.join(os.path.dirname(__file__), f'{module_name}.py')

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

DecodingStrategy = module.DecodingStrategy
MP3DecodingStrategy = module.MP3DecodingStrategy
WavDecodingStrategy = module.WavDecodingStrategy
MediaStreamingService = module.MediaStreamingService


class TestAudioDecoders(unittest.TestCase):
    def setUp(self):
        self.track_name = "awesome_song"

    def test_mp3_decoder_decode_stream(self):
        decoder = MP3DecodingStrategy()
        result = decoder.decode_stream(self.track_name)
        self.assertEqual(result, "Decoding MP3 frames using Fraunhofer algorithms.")

    def test_wav_decoder_decode_stream(self):
        decoder = WavDecodingStrategy()
        result = decoder.decode_stream(self.track_name)
        self.assertEqual(result, "Decoding raw PCM audio from WAV headers.")

class FakeDecodingStrategy(DecodingStrategy):
    def decode_stream(self, track_name):
        return f"Fake decoding for {track_name}"

class TestMediaStreamingService(unittest.TestCase):
    def setUp(self):
        patcher = patch('builtins.print')
        self.mock_print = patcher.start()
        self.addCleanup(patcher.stop)

    def test_media_streaming_service_uses_mp3_strategy(self):
        service = MediaStreamingService(MP3DecodingStrategy())
        track_name = "awesome_song.mp3"
        result = service.play_track(track_name)
        self.mock_print.assert_called_once_with(f"MediaService: Buffering {track_name} into memory...")
        self.assertEqual(result,"Playing: Decoding MP3 frames using Fraunhofer algorithms.")

    def test_media_streaming_service_uses_wav_decoding_strategy(self):
        service = MediaStreamingService(WavDecodingStrategy())
        track_name = "awesome_song.wav"
        result = service.play_track(track_name)
        self.mock_print.assert_called_once_with(f"MediaService: Buffering {track_name} into memory...")
        self.assertEqual(result, "Playing: Decoding raw PCM audio from WAV headers.")

    def test_media_streaming_service_uses_generic_decoding_strategy(self):
        service = MediaStreamingService(FakeDecodingStrategy())
        track_name = "test_track.fake"
        result = service.play_track(track_name)
        self.mock_print.assert_called_once_with(f"MediaService: Buffering {track_name} into memory...")
        self.assertEqual(result, "Playing: Fake decoding for test_track.fake")

if __name__ == '__main__':
    unittest.main()
