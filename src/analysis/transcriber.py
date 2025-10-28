"""
Audio Transcription Service
Converts audio files to text using Whisper or Deepgram
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Transcriber:
    """Transcribe audio files to text"""

    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.deepgram_api_key = os.getenv('DEEPGRAM_API_KEY')

    def transcribe(self, audio_file_path):
        """
        Transcribe an audio file to text

        Args:
            audio_file_path: Path to the audio file

        Returns:
            Transcript text
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        # Try Deepgram first (faster and cheaper)
        if self.deepgram_api_key:
            return self._transcribe_with_deepgram(audio_file_path)

        # Fall back to OpenAI Whisper
        elif self.openai_api_key:
            return self._transcribe_with_whisper(audio_file_path)

        else:
            raise Exception("No transcription API key configured. Add OPENAI_API_KEY or DEEPGRAM_API_KEY to .env")

    def _transcribe_with_whisper(self, audio_file_path):
        """Transcribe using OpenAI Whisper API"""
        from openai import OpenAI

        client = OpenAI(api_key=self.openai_api_key)

        print("🎙️  Transcribing with Whisper...")

        with open(audio_file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

        print(f"✅ Transcription complete: {len(transcript)} characters")
        return transcript

    def _transcribe_with_deepgram(self, audio_file_path):
        """Transcribe using Deepgram API"""
        from deepgram import Deepgram
        import asyncio

        print("🎙️  Transcribing with Deepgram...")

        dg_client = Deepgram(self.deepgram_api_key)

        with open(audio_file_path, 'rb') as audio:
            source = {'buffer': audio, 'mimetype': 'audio/mp4'}
            options = {
                'punctuate': True,
                'model': 'nova-2',
                'language': 'en-US',
                'diarize': True,  # Speaker diarization
            }

            # Run async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                dg_client.transcription.prerecorded(source, options)
            )

        # Extract transcript
        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']

        print(f"✅ Transcription complete: {len(transcript)} characters")
        return transcript

    def transcribe_with_speakers(self, audio_file_path):
        """
        Transcribe with speaker identification
        Returns transcript with speaker labels
        """
        if self.deepgram_api_key:
            return self._transcribe_with_speakers_deepgram(audio_file_path)
        else:
            # Whisper doesn't support speaker diarization by default
            return self.transcribe(audio_file_path)

    def _transcribe_with_speakers_deepgram(self, audio_file_path):
        """Transcribe with speaker labels using Deepgram"""
        from deepgram import Deepgram
        import asyncio

        print("🎙️  Transcribing with speaker identification...")

        dg_client = Deepgram(self.deepgram_api_key)

        with open(audio_file_path, 'rb') as audio:
            source = {'buffer': audio, 'mimetype': 'audio/mp4'}
            options = {
                'punctuate': True,
                'model': 'nova-2',
                'language': 'en-US',
                'diarize': True,
                'utterances': True
            }

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                dg_client.transcription.prerecorded(source, options)
            )

        # Format with speakers
        utterances = response['results']['utterances']
        formatted_transcript = []

        for utterance in utterances:
            speaker = f"Speaker {utterance['speaker']}"
            text = utterance['transcript']
            formatted_transcript.append(f"{speaker}: {text}")

        transcript = "\n\n".join(formatted_transcript)

        print(f"✅ Transcription complete with {len(utterances)} utterances")
        return transcript


# Demo transcriber for testing without API keys
class DemoTranscriber:
    """Demo version that returns sample transcript"""

    def transcribe(self, audio_file_path):
        """Returns a demo transcript"""
        print("🤖 Demo Transcriber: Using sample transcript")
        print("⚠️  To use real transcription:")
        print("   1. Add OPENAI_API_KEY or DEEPGRAM_API_KEY to .env")
        print("   2. Run again with real API key")

        return """
Speaker 1: Good afternoon everyone, thanks for joining today's meeting. I wanted to discuss some concerns that have been raised by graduate students.

Speaker 2: Thank you for having us. I think the biggest issue right now is mental health resources. Many students are waiting 3 to 4 weeks for counseling appointments.

Speaker 3: I agree. As a PhD student, the stress of research combined with long wait times makes things really difficult. We need more specialized support for doctoral students.

Speaker 1: That's really concerning. Have others experienced this as well?

Speaker 4: Yes, I've heard similar feedback from students in my department. The wait times are definitely a problem.

Speaker 2: Another issue is housing costs. Many students are spending over 60% of their stipend on rent. It's becoming financially unsustainable.

Speaker 5: Absolutely. I had to move further away from campus because I couldn't afford the rent near MIT. Now my commute is over an hour each way.

Speaker 1: These are critical issues. Let me take these back to the council and we'll work on proposals for both mental health resources and housing support.

Speaker 3: Thank you. We appreciate you listening to our concerns.

Speaker 1: Of course. I'll follow up with everyone after next week's council meeting.
"""

    def transcribe_with_speakers(self, audio_file_path):
        """Returns demo transcript with speakers"""
        return self.transcribe(audio_file_path)
