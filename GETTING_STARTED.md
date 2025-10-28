# Getting Started with DelegateAI MVP

This guide will help you set up and run DelegateAI to transcribe Zoom meetings.

## Quick Start (5 minutes)

### 1. Install Python Dependencies

```bash
cd delegate-ai
pip install -r requirements.txt
```

### 2. Set Up API Keys

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys (see below for where to get them).

### 3. Run the Backend

```bash
python src/api/app.py
```

The API will start at `http://localhost:5000`

### 4. Open the Web Interface

Open `app/index.html` in your browser, or:
```bash
cd app
# Windows
start index.html

# Mac
open index.html

# Linux
xdg-open index.html
```

### 5. Submit a Zoom Link!

Paste a Zoom meeting URL and click "Join Meeting & Transcribe"

---

## Getting API Keys

### Required: Anthropic API (for AI analysis)

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Go to API Keys
4. Create a new key
5. Add to `.env`: `ANTHROPIC_API_KEY=your_key_here`

**Cost**: ~$0.01-0.05 per meeting analysis

### Option 1: Recall.ai (Easiest - Recommended for Zoom bot)

**What it does**: Joins Zoom meetings as a bot, records audio/video

1. Go to: https://www.recall.ai/
2. Sign up for an account
3. Get your API key from dashboard
4. Add to `.env`: `RECALL_API_KEY=your_key_here`

**Cost**: $0.20-0.40 per meeting hour
**Why use it**: Easiest way to create a Zoom bot. Handles all the complexity.

### Option 2: OpenAI Whisper (for transcription)

**What it does**: Converts audio to text

1. Go to: https://platform.openai.com/api-keys
2. Create an API key
3. Add to `.env`: `OPENAI_API_KEY=your_key_here`

**Cost**: $0.006 per minute of audio (~$0.36 per hour)

### Option 3: Deepgram (Alternative transcription - Faster & Cheaper)

**What it does**: Converts audio to text (faster than Whisper)

1. Go to: https://console.deepgram.com/
2. Sign up and get API key
3. Add to `.env`: `DEEPGRAM_API_KEY=your_key_here`

**Cost**: $0.0043 per minute (~$0.26 per hour)

---

## Testing Without API Keys (Demo Mode)

Want to see how it works without setting up APIs yet?

1. Just run the backend: `python src/api/app.py`
2. Open the web interface
3. Submit any Zoom link

The system will use **demo data** to show you how it works:
- Demo transcript (sample meeting conversation)
- Demo analysis (AI-generated insights)

Once you're ready to use real meetings, add the API keys above.

---

## Full Setup Guide

### Step 1: Python Environment (Recommended)

Create a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Edit `.env` file:

```bash
# Minimum required (for demo mode)
ANTHROPIC_API_KEY=your_anthropic_key

# For real Zoom meetings
RECALL_API_KEY=your_recall_key

# For transcription (choose one)
OPENAI_API_KEY=your_openai_key
# OR
DEEPGRAM_API_KEY=your_deepgram_key

# Database (default is fine for development)
DATABASE_URL=sqlite:///delegate-ai.db

# Flask settings
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this
```

### Step 3: Initialize Database

```bash
python -c "from src.api.app import app, db; app.app_context().push(); db.create_all(); print('✅ Database created')"
```

### Step 4: Run the Application

**Terminal 1** - Start the API server:
```bash
python src/api/app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

**Terminal 2** (optional) - Serve the frontend:
```bash
cd app
python -m http.server 8080
```

Then open: http://localhost:8080

Or just open `app/index.html` directly in your browser.

### Step 5: Submit Your First Meeting

1. Get a Zoom meeting link (can be your own meeting or one you're invited to)
2. Paste it into the web interface
3. Add meeting name and your name
4. Click "Join Meeting & Transcribe"

**Note**: The bot needs to be admitted if there's a waiting room. The meeting host will see "DelegateAI (Your Name)" join.

---

## How It Works

### Architecture

```
User submits Zoom link
        ↓
Flask API creates meeting record
        ↓
Recall.ai bot joins Zoom meeting
        ↓
Bot records audio/video
        ↓
Whisper/Deepgram transcribes audio
        ↓
Claude analyzes transcript
        ↓
Results displayed in web interface
```

### File Structure

```
delegate-ai/
├── src/
│   ├── api/
│   │   ├── app.py           # Main Flask API
│   │   └── database.py      # Database models
│   ├── bot/
│   │   └── meeting_bot.py   # Zoom bot logic
│   └── analysis/
│       ├── transcriber.py   # Audio → text
│       └── analyzer.py      # AI analysis
├── app/
│   └── index.html           # Web interface
├── requirements.txt         # Python dependencies
└── .env                     # API keys (create this)
```

### API Endpoints

**POST /api/meetings**
- Submit a new meeting
- Body: `{ "zoom_link": "...", "meeting_name": "...", "rep_name": "..." }`
- Returns: `{ "meeting_id": 1, "status": "pending" }`

**GET /api/meetings/:id**
- Get meeting details and results
- Returns: Transcript and analysis

**POST /api/meetings/:id/process**
- Manually trigger processing
- Returns: Transcript and analysis when complete

**GET /api/meetings**
- List all meetings

---

## Troubleshooting

### "RECALL_API_KEY not set"

You're trying to join a real meeting without Recall.ai configured. Either:
1. Sign up for Recall.ai and add the API key to `.env`
2. Use demo mode (it will automatically fall back)

### "ANTHROPIC_API_KEY not set"

Add your Anthropic API key to `.env` for AI analysis. Without it, you'll get demo analysis.

### "Failed to create bot"

Check:
- Recall.ai API key is correct
- You have credits in your Recall.ai account
- Zoom link is valid and meeting is active

### "No module named 'flask'"

Install requirements: `pip install -r requirements.txt`

### Port 5000 already in use

Change the port in `src/api/app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

And update the API URL in `app/index.html`:
```javascript
const API_URL = 'http://localhost:5001/api';
```

### Meeting not transcribing

- Check that the meeting has ended (bots can't transcribe live meetings instantly)
- Wait a few minutes after meeting ends for processing
- Check the Flask console for error messages

---

## Cost Breakdown (per 1-hour meeting)

| Service | Cost | Notes |
|---------|------|-------|
| Recall.ai (Zoom bot) | $0.20-0.40 | Bot joins and records |
| Whisper (transcription) | $0.36 | Audio → text |
| Deepgram (alternative) | $0.26 | Faster, cheaper |
| Claude (analysis) | $0.01-0.05 | AI insights |
| **Total per meeting** | **$0.57-0.81** | Very affordable! |

For monthly usage (assuming 20 meetings/month): **$11-16/month**

---

## Next Steps

### Make it Production-Ready

1. **Add authentication** - Protect your API
2. **Use PostgreSQL** - Instead of SQLite for production
3. **Add Celery** - For async processing (don't block API calls)
4. **Deploy backend** - Use Heroku, Railway, or AWS
5. **Deploy frontend** - Use Vercel or Netlify
6. **Add webhooks** - Get notified when meetings complete

### Add Features

- Email notifications when transcript is ready
- Search across all transcripts
- Export to PDF or Google Docs
- Integrate with calendar to auto-join scheduled meetings
- Multi-user support with authentication
- Dashboard with all meetings and analytics

---

## Support

### Documentation
- Recall.ai docs: https://docs.recall.ai/
- Anthropic docs: https://docs.anthropic.com/
- OpenAI Whisper: https://platform.openai.com/docs/guides/speech-to-text

### Get Help
- Check the GitHub issues: https://github.com/joeleesuh/delegate-ai/issues
- Review the code comments in `src/`
- Test with demo mode first before using real API keys

---

## Security Notes

⚠️ **Important**:
- Never commit `.env` file to git (it's in `.gitignore`)
- Keep API keys secret
- Always announce when a bot joins a meeting (privacy/consent)
- Check your organization's recording policies
- Zoom participants must consent to recording

---

**Ready to try it?** Start with Step 1 above and you'll be transcribing meetings in 5 minutes!
