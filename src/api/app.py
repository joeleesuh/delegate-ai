"""
DelegateAI Flask API
Main application entry point
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from src.bot.meeting_bot import MeetingBot
from src.analysis.transcriber import Transcriber
from src.analysis.analyzer import MeetingAnalyzer
from src.api.database import db, Meeting

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///delegate-ai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Initialize services
meeting_bot = MeetingBot()
transcriber = Transcriber()
analyzer = MeetingAnalyzer()


@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'DelegateAI API',
        'version': '1.0.0'
    })


@app.route('/api/meetings', methods=['POST'])
def create_meeting():
    """
    Submit a Zoom meeting link to be transcribed and analyzed

    Request body:
    {
        "zoom_link": "https://zoom.us/j/123456789",
        "meeting_name": "Optional meeting name",
        "rep_name": "Your name"
    }
    """
    data = request.json

    if not data or 'zoom_link' not in data:
        return jsonify({'error': 'zoom_link is required'}), 400

    zoom_link = data['zoom_link']
    meeting_name = data.get('meeting_name', 'Unnamed Meeting')
    rep_name = data.get('rep_name', 'Representative')

    try:
        # Create meeting record
        meeting = Meeting(
            zoom_link=zoom_link,
            meeting_name=meeting_name,
            rep_name=rep_name,
            status='pending'
        )
        db.session.add(meeting)
        db.session.commit()

        # Start async processing (in production, use Celery)
        # For now, we'll process synchronously for demo purposes
        # process_meeting.delay(meeting.id)

        return jsonify({
            'success': True,
            'meeting_id': meeting.id,
            'status': 'pending',
            'message': 'Meeting submitted for processing. Bot will join and record.'
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/meetings/<int:meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    """Get meeting details, transcript, and analysis"""
    meeting = Meeting.query.get_or_404(meeting_id)

    return jsonify({
        'id': meeting.id,
        'meeting_name': meeting.meeting_name,
        'zoom_link': meeting.zoom_link,
        'status': meeting.status,
        'transcript': meeting.transcript,
        'analysis': meeting.analysis,
        'created_at': meeting.created_at.isoformat() if meeting.created_at else None,
        'completed_at': meeting.completed_at.isoformat() if meeting.completed_at else None
    })


@app.route('/api/meetings', methods=['GET'])
def list_meetings():
    """List all meetings"""
    meetings = Meeting.query.order_by(Meeting.created_at.desc()).all()

    return jsonify({
        'meetings': [{
            'id': m.id,
            'meeting_name': m.meeting_name,
            'status': m.status,
            'created_at': m.created_at.isoformat() if m.created_at else None
        } for m in meetings]
    })


@app.route('/api/meetings/<int:meeting_id>/process', methods=['POST'])
def process_meeting(meeting_id):
    """
    Manually trigger processing for a meeting
    This joins the Zoom, records, transcribes, and analyzes
    """
    meeting = Meeting.query.get_or_404(meeting_id)

    if meeting.status == 'completed':
        return jsonify({'error': 'Meeting already processed'}), 400

    try:
        # Update status
        meeting.status = 'processing'
        db.session.commit()

        # Step 1: Join meeting and get recording
        print(f"Joining meeting: {meeting.zoom_link}")
        audio_file = meeting_bot.join_and_record(
            meeting.zoom_link,
            rep_name=meeting.rep_name
        )

        # Step 2: Transcribe audio
        print(f"Transcribing audio: {audio_file}")
        transcript = transcriber.transcribe(audio_file)
        meeting.transcript = transcript
        db.session.commit()

        # Step 3: Analyze with Claude
        print("Analyzing meeting with Claude...")
        analysis = analyzer.analyze_meeting(
            transcript=transcript,
            meeting_name=meeting.meeting_name
        )
        meeting.analysis = analysis

        # Update status
        meeting.status = 'completed'
        meeting.completed_at = db.func.now()
        db.session.commit()

        return jsonify({
            'success': True,
            'meeting_id': meeting.id,
            'status': 'completed',
            'transcript': transcript,
            'analysis': analysis
        })

    except Exception as e:
        meeting.status = 'failed'
        meeting.error_message = str(e)
        db.session.commit()
        return jsonify({'error': str(e)}), 500


@app.route('/api/transcribe', methods=['POST'])
def transcribe_direct():
    """
    Direct transcription endpoint for testing
    Upload an audio file to get transcript
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    try:
        # Save temporarily
        temp_path = f"/tmp/{audio_file.filename}"
        audio_file.save(temp_path)

        # Transcribe
        transcript = transcriber.transcribe(temp_path)

        # Clean up
        os.remove(temp_path)

        return jsonify({
            'success': True,
            'transcript': transcript
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
