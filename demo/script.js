// Navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        // Remove active class from all nav items
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));

        // Add active class to clicked item
        this.classList.add('active');

        // Hide all views
        document.querySelectorAll('.view').forEach(view => view.classList.remove('active'));

        // Show selected view
        const viewName = this.dataset.view;
        const view = document.getElementById(`${viewName}-view`);
        if (view) {
            view.classList.add('active');
        }

        // Update page title
        const titleMap = {
            'dashboard': 'Dashboard',
            'meetings': 'Meetings',
            'feedback': 'Constituent Feedback',
            'insights': 'Insights'
        };

        const subtitleMap = {
            'dashboard': 'Your constituent engagement overview',
            'meetings': 'AI-attended meetings and summaries',
            'feedback': 'Direct responses from your constituents',
            'insights': 'AI-powered patterns and recommendations'
        };

        document.querySelector('.page-title').textContent = titleMap[viewName];
        document.querySelector('.page-subtitle').textContent = subtitleMap[viewName];
    });
});

// Meeting detail data
const meetingDetails = {
    1: {
        title: 'MIT Sloan MBA Town Hall',
        meta: 'Today, 2:00 PM • 45 attendees • 78 minutes',
        summary: `
            <div class="modal-section">
                <h4>📋 Executive Summary</h4>
                <p>The Sloan MBA Town Hall focused on three primary areas: career services improvements, networking opportunities, and mental health resources. Overall sentiment was positive with constructive feedback.</p>
            </div>

            <div class="modal-section">
                <h4>🎯 Key Topics Discussed</h4>
                <ul>
                    <li><strong>Career Services (40 minutes):</strong> Students expressed satisfaction with new industry panel series. Request for more tech startup connections and international job search support.</li>
                    <li><strong>Networking Events (25 minutes):</strong> Positive feedback on alumni mixer format. Students want more cross-program events (MBA + Engineering).</li>
                    <li><strong>Mental Health Resources (13 minutes):</strong> Concerns about recruiting stress and work-life balance. Students want MBA-specific counseling options.</li>
                </ul>
            </div>

            <div class="modal-section">
                <h4>💬 Notable Quotes</h4>
                <div class="modal-quote">
                    "The new industry panel series has been incredibly valuable. Can we get more representation from tech startups and venture capital?"
                    <div style="margin-top: 0.5rem; font-weight: 600;">- 2nd year MBA student</div>
                </div>
                <div class="modal-quote">
                    "Recruiting season is intense. We need mental health resources specifically for MBA students dealing with job search stress and multiple deadlines."
                    <div style="margin-top: 0.5rem; font-weight: 600;">- 1st year MBA student</div>
                </div>
                <div class="modal-quote">
                    "I love the cross-functional aspect of MIT. More events that bring MBAs together with engineers and scientists would be amazing."
                    <div style="margin-top: 0.5rem; font-weight: 600;">- Sloan Fellow</div>
                </div>
            </div>

            <div class="modal-section">
                <h4>✅ Action Items</h4>
                <ul>
                    <li><strong>[HIGH PRIORITY]</strong> Connect with Career Services about expanding tech startup and VC recruiting resources</li>
                    <li><strong>[HIGH PRIORITY]</strong> Propose MBA-specific mental health counseling sessions focused on recruiting stress</li>
                    <li><strong>[MEDIUM]</strong> Work with other school GSC reps to organize cross-program networking events</li>
                </ul>
            </div>

            <div class="modal-section">
                <h4>📊 Sentiment Analysis</h4>
                <p><strong>Overall:</strong> <span class="sentiment positive">70% Positive, 25% Neutral, 5% Negative</span></p>
                <p style="margin-top: 0.5rem; color: var(--text-secondary);">Students are generally satisfied with current offerings but see clear opportunities for improvement. Mental health concerns, while only 5% negative sentiment, were raised with high urgency.</p>
            </div>

            <div class="modal-section">
                <h4>🎯 Recommendations for GSC</h4>
                <ul>
                    <li>Schedule follow-up meeting with Career Services Director within 2 weeks</li>
                    <li>Survey MBA students specifically about mental health needs during recruiting</li>
                    <li>Present cross-program event proposal at next GSC meeting</li>
                    <li>Share positive feedback with Career Services team to encourage continued innovation</li>
                </ul>
            </div>
        `
    },
    2: {
        title: 'EECS Department Meeting',
        meta: 'Yesterday, 4:00 PM • 62 attendees • 52 minutes',
        summary: `
            <div class="modal-section">
                <h4>📋 Executive Summary</h4>
                <p>EECS department meeting revealed significant concerns about course load, TA support, and mental health resources. Faculty and students both raised workload concerns. This is a high-priority issue requiring immediate attention.</p>
            </div>

            <div class="modal-section">
                <h4>🎯 Key Topics Discussed</h4>
                <ul>
                    <li><strong>Course Load & Requirements (30 minutes):</strong> PhD students feeling overwhelmed with coursework + research expectations. Discussion about reducing required courses or extending timeline.</li>
                    <li><strong>TA Support & Compensation (15 minutes):</strong> TAs requesting better training and compensation review. Students concerned about hours vs. compensation ratio.</li>
                    <li><strong>Mental Health Resources (7 minutes):</strong> CRITICAL - Multiple students reported 3-4 week wait times for counseling appointments. PhD students want specialized support for research stress and advisor relationships.</li>
                </ul>
            </div>

            <div class="modal-section">
                <h4>💬 Notable Quotes</h4>
                <div class="modal-quote">
                    "I've been trying to get a counseling appointment for three weeks. By the time I get in, my crisis moment has passed. We need better mental health support."
                    <div style="margin-top: 0.5rem; font-weight: 600;">- 4th year PhD student</div>
                </div>
                <div class="modal-quote">
                    "The pressure of coursework plus research plus TA duties is unsustainable. Something has to give, but we're afraid it will be our research progress."
                    <div style="margin-top: 0.5rem; font-weight: 600;">- 2nd year PhD student</div>
                </div>
                <div class="modal-quote">
                    "We need support specifically for PhD students dealing with advisor relationships and research setbacks. The general counseling doesn't address our unique challenges."
                    <div style="margin-top: 0.5rem; font-weight: 600;">- 3rd year PhD student</div>
                </div>
            </div>

            <div class="modal-section">
                <h4>✅ Action Items</h4>
                <ul>
                    <li><strong>[URGENT]</strong> Emergency request for increased mental health counseling capacity - bring to GSC immediately</li>
                    <li><strong>[URGENT]</strong> Propose PhD-specific mental health support program</li>
                    <li><strong>[HIGH]</strong> Work with EECS department on course load policy review</li>
                    <li><strong>[HIGH]</strong> Survey other departments to see if mental health wait times are university-wide issue</li>
                    <li><strong>[MEDIUM]</strong> Review TA compensation with administration</li>
                </ul>
            </div>

            <div class="modal-section">
                <h4>📊 Sentiment Analysis</h4>
                <p><strong>Overall:</strong> <span class="sentiment mixed">40% Positive, 35% Neutral, 25% Negative</span></p>
                <p style="margin-top: 0.5rem; color: var(--text-secondary);">Mixed sentiment with clear frustration about mental health resources and workload. Students appreciate department's willingness to discuss issues but want concrete action.</p>
            </div>

            <div class="modal-section">
                <h4>🚨 Critical Issues Identified</h4>
                <div style="background: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 0.5rem; border-left: 3px solid var(--danger-color);">
                    <strong>Mental Health Crisis:</strong> This is the 3rd meeting this week where mental health wait times were cited as critical issue. Recommend making this #1 priority for GSC emergency session.
                </div>
            </div>
        `
    },
    3: {
        title: 'Graduate Student Housing Forum',
        meta: 'Oct 24, 6:00 PM • 38 attendees • 65 minutes',
        summary: `
            <div class="modal-section">
                <h4>📋 Executive Summary</h4>
                <p>Housing forum revealed significant financial stress among graduate students due to rising Cambridge area rents. International students and those without family support particularly affected. Students seeking university intervention.</p>
            </div>

            <div class="modal-section">
                <h4>🎯 Key Topics Discussed</h4>
                <ul>
                    <li><strong>Rental Costs (35 minutes):</strong> Students reporting 50-60% of stipend going to rent. Multiple students considering leaving MIT due to financial unsustainability.</li>
                    <li><strong>On-Campus Housing Shortage (20 minutes):</strong> Waitlists for on-campus housing extending 18+ months. Students want priority system for international students and those with financial need.</li>
                    <li><strong>University Support Options (10 minutes):</strong> Discussion of housing subsidies, stipend increases, or expanded on-campus housing construction.</li>
                </ul>
            </div>

            <div class="modal-section">
                <h4>💬 Notable Quotes</h4>
                <div class="modal-quote">
                    "I'm paying $2,200/month for a studio in Cambridge. That's 62% of my monthly stipend before food or anything else. I'm considering leaving MIT."
                    <div style="margin-top: 0.5rem; font-weight: 600;">- International PhD student, Biology</div>
                </div>
                <div class="modal-quote">
                    "As an international student, I can't live with family or get support from home easily. The housing costs here are making it impossible to focus on research."
                    <div style="margin-top: 0.5rem; font-weight: 600;">- 1st year Master's student</div>
                </div>
            </div>

            <div class="modal-section">
                <h4>✅ Action Items</h4>
                <ul>
                    <li><strong>[HIGH]</strong> Compile housing cost data from graduate students across all departments</li>
                    <li><strong>[HIGH]</strong> Research housing subsidy programs at peer institutions (Stanford, Harvard, etc.)</li>
                    <li><strong>[MEDIUM]</strong> Propose pilot housing subsidy program to administration</li>
                    <li><strong>[MEDIUM]</strong> Request meeting with housing office about grad student priority system</li>
                </ul>
            </div>

            <div class="modal-section">
                <h4>📊 Sentiment Analysis</h4>
                <p><strong>Overall:</strong> <span class="sentiment negative">15% Positive, 30% Neutral, 55% Negative</span></p>
                <p style="margin-top: 0.5rem; color: var(--text-secondary);">Predominantly negative sentiment reflecting real financial hardship. Students appreciate forum but want concrete solutions, not just discussion.</p>
            </div>
        `
    }
};

// Show meeting detail modal
function showMeetingDetail(meetingId) {
    const modal = document.getElementById('meeting-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');

    const meeting = meetingDetails[meetingId];
    if (meeting) {
        modalTitle.textContent = meeting.title;
        modalBody.innerHTML = `
            <div style="color: var(--text-secondary); margin-bottom: 1.5rem;">${meeting.meta}</div>
            ${meeting.summary}
        `;
        modal.classList.add('active');
    }
}

// Close meeting detail modal
function closeMeetingDetail() {
    const modal = document.getElementById('meeting-modal');
    modal.classList.remove('active');
}

// Close modal when clicking outside
document.getElementById('meeting-modal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeMeetingDetail();
    }
});

// Add click handlers to "View Summary" buttons in activity list
document.addEventListener('DOMContentLoaded', function() {
    const activityButtons = document.querySelectorAll('.activity-item .btn-view');
    activityButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            // Map activity items to meeting IDs
            // First activity = meeting 1, second activity = skip (it's survey), third = meeting 2
            const meetingMap = [1, null, 2];
            const meetingId = meetingMap[index];
            if (meetingId) {
                showMeetingDetail(meetingId);
            }
        });
    });

    // Animate stats on load
    animateValue('stat-meetings', 0, 12, 1000);
    animateValue('stat-constituents', 0, 847, 1500);
    animateValue('stat-issues', 0, 43, 1200);
});

// Animate number counting
function animateValue(id, start, end, duration) {
    const element = document.querySelector(`[data-stat="${id}"]`);
    if (!element) return;

    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

// Add some hover effects and animations
document.querySelectorAll('.stat-card, .meeting-card, .insight-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px)';
    });

    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

console.log('🤖 DelegateAI Demo loaded successfully!');
console.log('💡 This is a demo interface showing how DelegateAI helps student government representatives engage with constituents at scale.');
