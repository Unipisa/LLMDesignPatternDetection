import unittest
from unittest.mock import patch
import os
import sys
import importlib.util

# Load the module dynamically since it starts with a number
module_name = 'mediastreaming_refactored_fm'
module_path = "/Users/alessandrofiumano/Documents/LLMDesignPatternDetection/end_to_end_refactoring/results/refactorer/mediastreaming_factory_method/mediastreaming_e2e_fm.py"

spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

AudioDecoder = module.AudioDecoder
MP3Decoder = module.MP3Decoder
WAVDecoder = module.WAVDecoder
MediaStreamingService = module.MediaStreamingService
MP3StreamingService = module.MP3StreamingService
WAVStreamingService = module.WAVStreamingService

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
