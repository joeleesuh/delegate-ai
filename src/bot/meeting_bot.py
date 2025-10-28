"""
Zoom Meeting Bot
Joins Zoom meetings, records audio, and saves for transcription

Note: This uses Recall.ai API which is the easiest way to create Zoom bots.
Alternative: Use Zoom Meeting SDK directly (more complex)
"""
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()


class MeetingBot:
    """Bot that joins Zoom meetings and records them"""

    def __init__(self):
        self.recall_api_key = os.getenv('RECALL_API_KEY')
        self.api_base = 'https://api.recall.ai/api/v1'

    def join_and_record(self, zoom_link, rep_name='Representative'):
        """
        Join a Zoom meeting and record it

        Args:
            zoom_link: The Zoom meeting URL
            rep_name: Name of the representative (for bot intro)

        Returns:
            Path to the recorded audio file
        """
        if not self.recall_api_key:
            raise Exception("RECALL_API_KEY not set. Please add it to your .env file.")

        # Create bot via Recall.ai
        bot_name = f"DelegateAI ({rep_name})"
        intro_message = f"Hi everyone! I'm DelegateAI, representing {rep_name}. I'm here to listen and take notes on their behalf."

        headers = {
            'Authorization': f'Token {self.recall_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'meeting_url': zoom_link,
            'bot_name': bot_name,
            'join_at': None,  # Join immediately
            'real_time_transcription': {
                'destination_url': None  # We'll download later
            },
            'automatic_leave': {
                'waiting_room_timeout': 600,  # Leave after 10 min in waiting room
                'noone_joined_timeout': 600  # Leave if no one joins for 10 min
            },
            'recording_mode': 'speaker_view',
            'transcription_options': {
                'provider': 'deepgram'
            }
        }

        # Create bot
        response = requests.post(
            f'{self.api_base}/bot',
            headers=headers,
            json=payload
        )

        if response.status_code != 201:
            raise Exception(f"Failed to create bot: {response.text}")

        bot_data = response.json()
        bot_id = bot_data['id']

        print(f"✅ Bot created: {bot_id}")
        print(f"⏳ Bot is joining the meeting...")

        # Poll for bot status
        while True:
            status_response = requests.get(
                f'{self.api_base}/bot/{bot_id}',
                headers=headers
            )

            if status_response.status_code != 200:
                raise Exception(f"Failed to get bot status: {status_response.text}")

            status_data = status_response.json()
            status = status_data['status_changes'][-1]['code']

            print(f"📊 Bot status: {status}")

            if status == 'in_call_not_recording':
                print("🎥 Bot joined! Starting recording...")

            elif status == 'in_call_recording':
                print("⏺️  Bot is recording the meeting...")
                # In production, you'd wait for the meeting to end
                # For demo, we'll just note that it's recording
                break

            elif status in ['fatal', 'done']:
                print("✅ Recording complete!")
                break

            time.sleep(5)  # Check every 5 seconds

        # Download the recording
        # Note: This is available after the meeting ends
        video_url = status_data.get('video_url')
        if video_url:
            audio_file = self._download_recording(video_url, bot_id)
            return audio_file
        else:
            # Meeting is still ongoing
            return f"recordings/bot_{bot_id}_pending.mp4"

    def _download_recording(self, video_url, bot_id):
        """Download the recording from Recall.ai"""
        os.makedirs('recordings', exist_ok=True)
        audio_file = f'recordings/bot_{bot_id}.mp4'

        response = requests.get(video_url, stream=True)
        with open(audio_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"💾 Recording saved: {audio_file}")
        return audio_file

    def get_bot_status(self, bot_id):
        """Get the status of a bot"""
        if not self.recall_api_key:
            raise Exception("RECALL_API_KEY not set")

        headers = {
            'Authorization': f'Token {self.recall_api_key}'
        }

        response = requests.get(
            f'{self.api_base}/bot/{bot_id}',
            headers=headers
        )

        if response.status_code != 200:
            raise Exception(f"Failed to get bot status: {response.text}")

        return response.json()


# Alternative: Simple demo version for testing without Recall.ai
class DemoMeetingBot:
    """Demo version that simulates joining a meeting"""

    def join_and_record(self, zoom_link, rep_name='Representative'):
        """
        Simulates joining a meeting (for demo purposes)
        In production, use the real MeetingBot with Recall.ai
        """
        print(f"🤖 Demo Bot: Would join meeting: {zoom_link}")
        print(f"👤 Representing: {rep_name}")
        print("⚠️  This is a demo. To actually join meetings:")
        print("   1. Sign up for Recall.ai: https://www.recall.ai/")
        print("   2. Add RECALL_API_KEY to your .env file")
        print("   3. Run again with real API key")

        # Return a demo audio file path
        return "demo/sample_meeting.mp3"
