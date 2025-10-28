"""
Meeting Analysis using Claude API
Analyzes transcripts to extract insights, action items, and sentiment
"""
import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class MeetingAnalyzer:
    """Analyze meeting transcripts using Claude"""

    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("⚠️  Warning: ANTHROPIC_API_KEY not set")
            self.client = None
        else:
            self.client = Anthropic(api_key=api_key)

    def analyze_meeting(self, transcript, meeting_name="Meeting"):
        """
        Analyze a meeting transcript and extract insights

        Args:
            transcript: The meeting transcript text
            meeting_name: Name of the meeting

        Returns:
            JSON string with analysis results
        """
        if not self.client:
            return self._demo_analysis()

        prompt = f"""Analyze this meeting transcript and provide a comprehensive summary in JSON format.

Meeting: {meeting_name}

Transcript:
{transcript}

Please provide a JSON response with the following structure:
{{
    "executive_summary": "Brief 2-3 sentence summary of the meeting",
    "key_topics": [
        {{
            "topic": "Topic name",
            "description": "What was discussed",
            "time_spent": "Approximate time or importance"
        }}
    ],
    "issues_identified": [
        {{
            "title": "Issue title",
            "description": "Detailed description",
            "category": "mental_health|housing|funding|academic|career|other",
            "priority": "high|medium|low",
            "sentiment": "positive|neutral|negative",
            "mentioned_by": "Who raised it"
        }}
    ],
    "action_items": [
        {{
            "action": "What needs to be done",
            "priority": "high|medium|low",
            "owner": "Who should do it (if mentioned)"
        }}
    ],
    "notable_quotes": [
        {{
            "quote": "The actual quote",
            "speaker": "Who said it",
            "context": "Why it's important"
        }}
    ],
    "sentiment_analysis": {{
        "overall": "positive|mixed|negative",
        "breakdown": {{
            "positive_percent": 0,
            "neutral_percent": 0,
            "negative_percent": 0
        }},
        "explanation": "Brief explanation of the sentiment"
    }},
    "recommendations": [
        "Specific actionable recommendation for the representative"
    ],
    "patterns": [
        "Any patterns or trends observed"
    ]
}}

Provide only the JSON response, no additional text."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract JSON from response
            response_text = message.content[0].text

            # Try to parse as JSON
            analysis = json.loads(response_text)

            print("✅ Meeting analysis complete")
            return json.dumps(analysis, indent=2)

        except json.JSONDecodeError:
            # If response isn't valid JSON, wrap it
            return json.dumps({
                "executive_summary": response_text[:500],
                "error": "Failed to parse structured analysis"
            })
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return json.dumps({"error": str(e)})

    def extract_issues(self, transcript):
        """Extract just the issues from a transcript"""
        if not self.client:
            return []

        prompt = f"""Extract all issues, concerns, or problems mentioned in this meeting transcript.

Transcript:
{transcript}

For each issue, provide:
- Title (brief, 5-10 words)
- Description (detailed)
- Category (mental_health, housing, funding, academic, career, or other)
- Priority (high, medium, low based on urgency and frequency)
- Sentiment (how people feel about it)

Return as JSON array."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            issues = json.loads(message.content[0].text)
            return issues

        except Exception as e:
            print(f"❌ Issue extraction error: {e}")
            return []

    def _demo_analysis(self):
        """Return demo analysis for testing"""
        print("🤖 Demo Analyzer: Using sample analysis")
        print("⚠️  To use real analysis:")
        print("   1. Add ANTHROPIC_API_KEY to .env")
        print("   2. Run again with real API key")

        return json.dumps({
            "executive_summary": "Meeting discussed critical graduate student concerns including mental health resources and housing affordability. Multiple departments reported 3-4 week wait times for counseling appointments. Students spending 60%+ of stipends on rent.",
            "key_topics": [
                {
                    "topic": "Mental Health Resources",
                    "description": "Students reporting 3-4 week wait times for counseling. Need for PhD-specific support.",
                    "time_spent": "High importance, mentioned by multiple speakers"
                },
                {
                    "topic": "Housing Affordability",
                    "description": "Cambridge rent consuming 60%+ of stipends. Students considering leaving MIT.",
                    "time_spent": "Medium-high importance"
                }
            ],
            "issues_identified": [
                {
                    "title": "Mental Health Counseling Wait Times",
                    "description": "Students waiting 3-4 weeks for appointments. PhD students need specialized support for research stress.",
                    "category": "mental_health",
                    "priority": "high",
                    "sentiment": "negative",
                    "mentioned_by": "Multiple students across departments"
                },
                {
                    "title": "Housing Cost Burden",
                    "description": "Rent taking 60%+ of student stipends, particularly affecting international students without family nearby.",
                    "category": "housing",
                    "priority": "high",
                    "sentiment": "negative",
                    "mentioned_by": "Graduate students"
                }
            ],
            "action_items": [
                {
                    "action": "Bring mental health wait times to GSC as urgent priority",
                    "priority": "high",
                    "owner": "Representative"
                },
                {
                    "action": "Request meeting with Mental Health Services director",
                    "priority": "high",
                    "owner": "Representative"
                },
                {
                    "action": "Compile housing cost data from students",
                    "priority": "medium",
                    "owner": "Representative"
                }
            ],
            "notable_quotes": [
                {
                    "quote": "Many students are waiting 3 to 4 weeks for counseling appointments.",
                    "speaker": "Speaker 2",
                    "context": "Highlighting urgent mental health resource gap"
                },
                {
                    "quote": "Many students are spending over 60% of their stipend on rent. It's becoming financially unsustainable.",
                    "speaker": "Speaker 2",
                    "context": "Housing affordability crisis"
                }
            ],
            "sentiment_analysis": {
                "overall": "negative",
                "breakdown": {
                    "positive_percent": 10,
                    "neutral_percent": 25,
                    "negative_percent": 65
                },
                "explanation": "Predominantly negative sentiment reflecting serious concerns about mental health and housing. Students appreciate being heard but express frustration with current situation."
            },
            "recommendations": [
                "Schedule emergency GSC meeting to address mental health resource shortage",
                "Survey graduate students across all departments on mental health needs and wait times",
                "Research peer institution models for mental health support and housing subsidies",
                "Propose pilot housing subsidy program for graduate students",
                "Create task force to address both issues with administration"
            ],
            "patterns": [
                "Mental health concerns span multiple departments - suggests systemic university-wide issue",
                "Housing concerns disproportionately affect international students",
                "Students want action, not just discussion - emphasis on concrete solutions"
            ]
        }, indent=2)


# Quick test function
if __name__ == "__main__":
    analyzer = MeetingAnalyzer()

    sample_transcript = """
    Speaker 1: Thanks for joining. I wanted to discuss student concerns.
    Speaker 2: Mental health resources are a big issue. Students wait 3-4 weeks for appointments.
    Speaker 3: Yes, and housing costs are taking over 60% of our stipends.
    """

    analysis = analyzer.analyze_meeting(sample_transcript, "Test Meeting")
    print(json.dumps(json.loads(analysis), indent=2))
