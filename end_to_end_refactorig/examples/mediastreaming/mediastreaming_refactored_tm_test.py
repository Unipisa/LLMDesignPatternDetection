import unittest
from unittest.mock import patch, call
import os
import sys
import importlib.util

# Load the module dynamically since it starts with a number
module_name = 'mediastreaming_refactored_tm'
module_path = os.path.join(os.path.dirname(__file__), f'{module_name}.py')

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

MP3StreamingService = module.MP3StreamingService
WAVStreamingService = module.WAVStreamingService


class TestMediaStreamingServices(unittest.TestCase):

    def setUp(self):
        patcher = patch('builtins.print')
        self.mock_print = patcher.start()
        self.addCleanup(patcher.stop)

    def test_mp3_streaming_service_decode_stream(self):
        service = MP3StreamingService()
        result = service.decode_stream()
        self.assertEqual(result, "Decoding MP3 frames using Fraunhofer algorithms.")

    def test_wav_streaming_service_decode_stream(self):
        service = WAVStreamingService()
        result = service.decode_stream()
        self.assertEqual(result, "Decoding raw PCM audio from WAV headers.")

    def test_mp3_streaming_service_play_track(self):
        service = MP3StreamingService()
        track_name = "awesome_song.mp3"
        result = service.play_track(track_name)

        self.mock_print.assert_has_calls([
            call(f"MediaService: Buffering {track_name} into memory..."),
            call("Playing: Decoding MP3 frames using Fraunhofer algorithms.")
        ])
        self.assertEqual(self.mock_print.call_count, 2)
        self.assertIsNone(result)

    def test_wav_streaming_service_play_track(self):
        service = WAVStreamingService()
        track_name = "lossless_song.wav"
        result = service.play_track(track_name)

        self.mock_print.assert_has_calls([
            call(f"MediaService: Buffering {track_name} into memory..."),
            call("Playing: Decoding raw PCM audio from WAV headers.")
        ])
        self.assertEqual(self.mock_print.call_count, 2)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
