# DelegateAI MVP Specification

## Vision
An AI agent that helps MIT GSC At-Large Representatives (and eventually all organizational representatives) engage with constituents at scale by attending meetings and gathering feedback.

## Target User (Phase 1)
**Primary**: You - MIT Sloan MBA, At-Large Representative on MIT Graduate Student Council
**Secondary**: Other student government representatives at MIT and other universities

## Core User Stories

### Story 1: Zoom Meeting Attendance
**As a** GSC representative
**I want** my AI agent to attend constituent Zoom meetings on my behalf
**So that** I can be "present" at multiple events simultaneously and not miss important discussions

**Acceptance Criteria:**
- Agent can join Zoom meeting via link/calendar invite
- Agent introduces itself (e.g., "Hi, I'm DelegateAI representing [Your Name], here to listen and take notes")
- Agent records and transcribes the full meeting
- Agent generates a structured summary with:
  - Key topics discussed
  - Constituent concerns raised
  - Action items mentioned
  - Notable quotes
  - Sentiment analysis

### Story 2: Constituent Feedback Collection
**As a** GSC representative
**I want** to proactively ask my constituents what they care about
**So that** I can represent their interests effectively

**Acceptance Criteria:**
- Simple survey system that asks: "What matters most to you as an MIT grad student?"
- Follow-up questions based on initial response
- Categorizes responses by theme (housing, mental health, funding, etc.)
- Tracks sentiment and urgency
- Shows trends over time

### Story 3: Insights Dashboard
**As a** GSC representative
**I want** a simple dashboard to review all constituent insights
**So that** I can quickly understand what my constituents need

**Acceptance Criteria:**
- List of meetings attended with summaries
- Survey responses organized by topic
- Top issues/themes across all inputs
- Ability to drill down into specific meetings or responses
- Export capabilities for council reports

## MVP Features (Detailed)

### 1. Zoom Bot Integration
**Priority:** P0 (Must have)

**Functionality:**
- Accept Zoom meeting link
- Join meeting as "bot" participant
- Announce presence with customizable intro message
- Record audio (with participant consent/notification)
- Leave meeting gracefully with closing message

**Technical Requirements:**
- Zoom SDK/API integration
- Meeting bot infrastructure (headless browser or native SDK)
- Audio recording capabilities
- Compliance with Zoom's bot policies

**Out of Scope for MVP:**
- Video recording
- Speaking/asking questions during meeting
- Real-time responses

### 2. Transcription & Analysis
**Priority:** P0 (Must have)

**Functionality:**
- Transcribe meeting audio to text
- Identify speakers (or note as "Speaker 1, 2, etc.")
- Extract key information:
  - Main topics discussed
  - Problems/concerns raised
  - Suggestions/requests
  - Action items
  - Sentiment (positive/negative/neutral)
  - Notable quotes

**Technical Requirements:**
- Speech-to-text service (Whisper, Deepgram, or similar)
- Claude API for content analysis
- Structured output format (JSON)

**Out of Scope for MVP:**
- Real-time transcription during meeting
- Perfect speaker identification
- Multi-language support

### 3. Survey System
**Priority:** P0 (Must have)

**Functionality:**
- Create simple text-based surveys
- Send via email or shareable link
- Questions:
  - "What matters most to you as an MIT grad student?"
  - "Are there any specific issues you'd like me to address?"
  - "Rate your satisfaction with [topic]"
- AI-generated follow-up questions based on responses
- Store responses in database

**Technical Requirements:**
- Simple form builder or use existing survey tool
- Email integration
- Claude API for generating contextual follow-ups
- Database schema for responses

**Out of Scope for MVP:**
- Complex survey logic
- Multimedia responses
- Anonymous response handling (can add later)

### 4. Dashboard
**Priority:** P0 (Must have)

**Functionality:**
- Login/authentication (simple, just for you initially)
- Meeting list with summaries
- Survey response viewer
- Top themes/issues aggregated view
- Search/filter by topic, date, source
- Export to PDF or markdown

**Technical Requirements:**
- Simple React or Vue frontend
- RESTful API backend
- Basic authentication
- Data visualization library (charts for trends)

**Out of Scope for MVP:**
- Mobile app
- Real-time updates
- Complex analytics
- Multi-user support (add in Phase 2)

### 5. Constituent Intelligence
**Priority:** P1 (Should have)

**Functionality:**
- Track issues mentioned across multiple meetings/surveys
- Identify patterns (e.g., "Housing mentioned in 5/8 meetings")
- Flag urgent concerns based on sentiment/frequency
- Group similar feedback together
- Generate weekly digest

**Technical Requirements:**
- Claude API for pattern recognition
- Simple topic modeling or clustering
- Alert/notification system

**Out of Scope for MVP:**
- Predictive analytics
- Constituent profiles/demographics
- Network analysis

## Technical Architecture (High-Level)

```
┌─────────────────┐
│  Zoom Meeting   │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Zoom Bot │
    └────┬─────┘
         │
    ┌────▼──────────┐
    │ Transcription │
    │   Service     │
    └────┬──────────┘
         │
    ┌────▼─────────┐         ┌──────────┐
    │   Claude API  │◄────────┤ Surveys  │
    │   (Analysis)  │         └──────────┘
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │   Database    │
    │  (PostgreSQL) │
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │   Dashboard   │
    │   (React)     │
    └───────────────┘
```

## Success Metrics

### Engagement Metrics
- Number of meetings attended per week
- Survey response rate
- Number of unique constituent interactions

### Quality Metrics
- Accuracy of meeting summaries (self-reported)
- Usefulness of insights (self-reported)
- Time saved vs. attending manually

### Impact Metrics
- Number of constituent issues identified
- Issues successfully addressed in council
- Constituent satisfaction (quarterly survey)

## MVP Timeline (6-week sprint)

### Week 1-2: Foundation
- Set up development environment
- Design database schema
- Build basic API structure
- Create simple dashboard shell

### Week 3-4: Zoom Integration
- Implement Zoom bot
- Integrate transcription service
- Build meeting summary pipeline
- Test with sample meetings

### Week 5: Survey & Analysis
- Build survey system
- Implement Claude analysis
- Create insights aggregation
- Dashboard data integration

### Week 6: Polish & Test
- User testing (with you)
- Bug fixes
- Documentation
- Prepare for first real use

## Beyond MVP (Future Phases)

### Phase 2: Intelligence (Months 2-3)
- Proactive issue identification
- Constituent clustering by concerns
- Automated follow-ups based on action items
- Integration with calendar for auto-joining

### Phase 3: Scale (Months 4-6)
- Multi-representative support (entire GSC)
- Analytics and reporting suite
- Mobile app
- Integration with MIT systems

### Phase 4: Market Expansion
- Other universities
- Professional associations
- Community boards
- Elected officials

## Business Model (Future)

### For MVP: Free (personal use)

### For Scale:
- **Freemium**: Basic features free, advanced analytics paid
- **Tier 1** ($29/month): Individual representative
- **Tier 2** ($99/month): Organization (5-10 reps)
- **Tier 3** ($299/month): Institution (unlimited reps)
- **Enterprise**: Custom pricing for governments/large orgs

## Key Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Zoom bot violates terms of service | Research Zoom SDK compliance; always announce bot presence |
| Privacy concerns with recording | Require explicit consent; secure data storage; clear privacy policy |
| Poor transcription quality | Use high-quality service; manual review for critical meetings |
| Low constituent engagement | Start with engaging questions; iterate based on feedback |
| Technical complexity too high | Start with simplest version; use managed services where possible |

## Questions to Answer

1. Which Zoom SDK/approach is most reliable for meeting bots?
2. What's the best transcription service for academic/formal meetings?
3. How to handle consent/privacy for recording?
4. Should we integrate with MIT systems (Touchstone, etc.) or stay standalone?
5. What's the minimum viable dashboard for your needs?

## Next Steps

1. Validate this spec with you (the user)
2. Choose tech stack and services
3. Set up development environment
4. Build skeleton application
5. Start with Week 1-2 tasks

---

**Last Updated:** 2025-10-27
**Status:** Draft for review
