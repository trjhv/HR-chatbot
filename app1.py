import streamlit as st
import anthropic
import os
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="HR Assistant | Acme Corp",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium design
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');
    
    /* Root variables */
    :root {
        --primary-color: #2C5F7C;
        --secondary-color: #F4A261;
        --accent-color: #E76F51;
        --bg-primary: #FAFBFC;
        --bg-secondary: #FFFFFF;
        --text-primary: #1A2332;
        --text-secondary: #5A6C7D;
        --border-color: #E1E8ED;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.04);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.08);
        --shadow-lg: 0 8px 32px rgba(0,0,0,0.12);
    }
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #FAFBFC 0%, #F0F4F8 100%);
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main title styling */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #2C5F7C 0%, #4A90B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: fadeInDown 0.6s ease-out;
    }
    
    .subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.2rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        font-weight: 400;
        animation: fadeInUp 0.6s ease-out 0.2s both;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, rgba(44,95,124,0.05) 0%, rgba(74,144,184,0.05) 100%);
        border-radius: 24px;
        padding: 3rem;
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
        animation: fadeIn 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(244,162,97,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    /* Chat container */
    .chat-container {
        background: var(--bg-secondary);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-md);
        margin: 2rem 0;
        border: 1px solid var(--border-color);
        animation: slideUp 0.5s ease-out;
        min-height: 500px;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
        animation: messageSlideIn 0.4s ease-out;
    }
    
    .stChatMessage:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    /* User message */
    [data-testid="stChatMessageContent"] {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: var(--text-primary);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFB 100%);
        border-right: 1px solid var(--border-color);
        box-shadow: 4px 0 16px rgba(0,0,0,0.04);
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        padding: 2rem 1rem;
    }
    
    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        color: var(--primary-color);
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-primary);
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, #4A90B8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        background: linear-gradient(135deg, #4A90B8 0%, var(--primary-color) 100%);
    }
    
    /* Secondary buttons (sidebar) */
    [data-testid="stSidebar"] .stButton > button {
        background: white;
        color: var(--primary-color);
        border: 2px solid var(--border-color);
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: var(--bg-primary);
        border-color: var(--primary-color);
        color: var(--primary-color);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid var(--border-color);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(44,95,124,0.1);
    }
    
    /* Chat input */
    .stChatInput {
        border-radius: 16px;
        border: 2px solid var(--border-color);
        background: white;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .stChatInput:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(44,95,124,0.1);
    }
    
    /* Info/Warning boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        padding: 1rem 1.5rem;
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--border-color) 50%, transparent 100%);
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-4px);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Quick question pills */
    .quick-question {
        display: inline-block;
        background: white;
        border: 2px solid var(--border-color);
        border-radius: 24px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: var(--text-primary);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-question:hover {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
        transform: translateY(-2px);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: var(--primary-color) !important;
    }
    
    /* Success/Error messages */
    .success-message {
        background: linear-gradient(135deg, #D4EDDA 0%, #C3E6CB 100%);
        color: #155724;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #28A745;
        font-family: 'DM Sans', sans-serif;
    }
    
    .error-message {
        background: linear-gradient(135deg, #F8D7DA 0%, #F5C6CB 100%);
        color: #721C24;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #DC3545;
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, white 0%, #F8FAFB 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
    }
    
    .stat-number {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
"""

# HR System Prompt
HR_SYSTEM_PROMPT = """You are a helpful and professional HR assistant chatbot for Acme Corporation. Your role is to:

1. Answer questions about company policies, benefits, and procedures
2. Help with common HR inquiries like leave requests, benefits enrollment, and onboarding
3. Provide information about company culture and values
4. Direct employees to appropriate resources or departments for complex issues
5. Maintain confidentiality and professionalism at all times

Key HR Topics You Can Help With:
- Paid Time Off (PTO) and leave policies
- Health insurance and benefits
- 401(k) retirement plans
- Employee onboarding and offboarding
- Performance reviews and feedback
- Company holidays and work schedules
- Remote work policies
- Employee development and training
- Workplace policies and code of conduct
- Payroll and compensation questions

Guidelines:
- Be empathetic and supportive
- Provide clear, accurate information
- If you don't know something, admit it and suggest who to contact
- For sensitive issues (harassment, discrimination, legal matters), direct to appropriate HR personnel
- Respect employee privacy and confidentiality
- Use a warm, professional tone
- Break down complex policies into easy-to-understand points

Remember: You are a helpful assistant, not a replacement for human HR professionals. Complex or sensitive matters should be escalated to the HR department.
"""

# Sample HR Knowledge Base
HR_KNOWLEDGE = """
COMPANY INFORMATION:
- Company Name: Acme Corporation
- Founded: 1985
- Employees: 500+
- HR Email: hr@acmecorp.com
- HR Phone: (555) 123-4567
- HR Office Hours: Monday-Friday, 9 AM - 5 PM EST
- HR Portal: portal.acmecorp.com

PTO POLICY:
- New employees (0-2 years): 15 days per year
- Employees with 3-4 years: 20 days per year
- Employees with 5+ years: 25 days per year
- PTO accrues monthly
- PTO requests should be submitted at least 2 weeks in advance
- Submit requests through the HR portal or email hr@acmecorp.com
- Maximum rollover: 5 days per year
- Sick leave: Separate pool of 10 days per year

HEALTH INSURANCE:
- Coverage begins first day of the month following hire date
- Three plan options:
  * Basic Plan: $50/month employee contribution, $3,000 deductible
  * Standard Plan: $150/month employee contribution, $1,500 deductible
  * Premium Plan: $250/month employee contribution, $500 deductible
- All plans include dental and vision
- Open enrollment: November 1-30 each year
- Dependents can be added during open enrollment or within 30 days of qualifying life event
- HSA and FSA options available
- Mental health coverage included

401(k) PLAN:
- Eligible after 90 days of employment
- Company matches 50% of contributions up to 6% of salary
- Immediate vesting of employee contributions
- Company match vests over 3 years (33% per year)
- Multiple investment options available
- Can contribute up to IRS maximum ($23,000 for 2024)
- Roth 401(k) option available

COMPANY HOLIDAYS (2024):
- New Year's Day (January 1)
- Memorial Day (Last Monday in May)
- Independence Day (July 4)
- Labor Day (First Monday in September)
- Thanksgiving (Fourth Thursday in November)
- Day after Thanksgiving
- Christmas Eve (December 24)
- Christmas Day (December 25)
- Plus 2 floating holidays per year (employee's choice)

REMOTE WORK POLICY:
- Hybrid policy: 2-3 days in office per week (Tuesday, Wednesday required)
- Full remote available for approved roles and manager approval
- Remote work agreement required (renewable annually)
- Home office stipend: $500/year for equipment
- Internet reimbursement: Up to $50/month
- Co-working space reimbursement available if needed
- Must be available during core hours: 10 AM - 3 PM EST

PROFESSIONAL DEVELOPMENT:
- Annual learning budget: $2,000 per employee
- Conference attendance: Up to 2 per year
- LinkedIn Learning access provided
- Internal training programs quarterly
- Tuition reimbursement: Up to $5,000/year for approved programs
- Mentorship program available

PERFORMANCE REVIEWS:
- Annual reviews in December
- Mid-year check-ins in June
- 360-degree feedback process
- Goal setting using OKR framework
- Career development discussions included
- Compensation reviews tied to performance

ONBOARDING:
- 2-week structured onboarding program
- Buddy system for first 90 days
- IT setup on day one
- Benefits enrollment in first week
- Regular check-ins with manager and HR

PARENTAL LEAVE:
- 12 weeks paid leave for primary caregiver
- 4 weeks paid leave for secondary caregiver
- Can be taken within first year of birth/adoption
- Gradual return-to-work options available
"""

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False

def get_claude_response(messages, api_key):
    """Get response from Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        system_message = f"{HR_SYSTEM_PROMPT}\n\nHR KNOWLEDGE BASE:\n{HR_KNOWLEDGE}"
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_message,
            messages=messages
        )
        
        return response.content[0].text
    except anthropic.AuthenticationError:
        return "❌ Authentication failed. Please check your API key."
    except anthropic.APIError as e:
        return f"❌ API Error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def render_hero_section():
    """Render hero section with branding"""
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">HR Assistant</h1>
        <p class="subtitle">Your 24/7 guide to company policies, benefits, and more</p>
    </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render feature cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <div class="feature-title">Policy Guidance</div>
            <div class="feature-desc">Get instant answers about PTO, benefits, and company policies</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💼</div>
            <div class="feature-title">Benefits Info</div>
            <div class="feature-desc">Learn about health insurance, 401(k), and other benefits</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Quick Support</div>
            <div class="feature-desc">Fast, helpful responses to your HR questions anytime</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Inject custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Anthropic API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your Anthropic API key",
            placeholder="sk-ant-..."
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.markdown('<div class="success-message">✅ API Key configured</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">⚠️ Please enter your API key</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        stat_col1, stat_col2 = st.columns(2)
        
        with stat_col1:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-number">500+</div>
                <div class="stat-label">Employees</div>
            </div>
            """, unsafe_allow_html=True)
        
        with stat_col2:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Available</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Resources
        st.markdown("### 📚 Quick Links")
        st.markdown("""
        <div style="padding: 0.5rem 0;">
            • <a href="#" style="color: var(--primary-color); text-decoration: none;">HR Portal</a><br>
            • <a href="#" style="color: var(--primary-color); text-decoration: none;">Benefits Guide</a><br>
            • <a href="#" style="color: var(--primary-color); text-decoration: none;">Employee Handbook</a><br>
            • <a href="#" style="color: var(--primary-color); text-decoration: none;">Submit PTO Request</a><br>
            • <a href="mailto:hr@acmecorp.com" style="color: var(--primary-color); text-decoration: none;">Contact HR</a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Common Questions
        st.markdown("### 💡 Common Questions")
        common_questions = [
            "How do I request time off?",
            "What are the health insurance options?",
            "How does 401(k) matching work?",
            "What are the company holidays?",
            "What is the remote work policy?",
            "How do I enroll in benefits?"
        ]
        
        for question in common_questions:
            if st.button(question, key=f"btn_{question}", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })
                st.session_state.chat_started = True
                st.rerun()
        
        st.markdown("---")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.chat_started = False
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: var(--text-secondary); font-size: 0.8rem; padding: 1rem 0;">
            <p>Acme Corporation<br>HR Department</p>
            <p style="margin-top: 0.5rem;">📧 hr@acmecorp.com<br>📞 (555) 123-4567</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    if not st.session_state.chat_started:
        # Welcome screen
        render_hero_section()
        render_features()
        
        st.markdown("### 🚀 Get Started")
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 2rem; border: 1px solid var(--border-color); box-shadow: var(--shadow-sm);">
            <p style="font-size: 1.1rem; color: var(--text-primary); margin-bottom: 1rem;">
                Welcome to the Acme HR Assistant! I'm here to help you with:
            </p>
            <ul style="color: var(--text-secondary); line-height: 1.8;">
                <li>Understanding company policies and benefits</li>
                <li>Answering questions about PTO and leave</li>
                <li>Explaining health insurance and 401(k) options</li>
                <li>Guidance on remote work and professional development</li>
                <li>General HR support and resources</li>
            </ul>
            <p style="font-size: 1rem; color: var(--text-primary); margin-top: 1.5rem;">
                💬 Start by asking a question below or select from common questions in the sidebar.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Chat interface
        st.markdown('<h2 style="font-family: \'Playfair Display\', serif; color: var(--primary-color); margin-bottom: 2rem;">💬 Conversation</h2>', unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about HR policies, benefits, or procedures..."):
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your Anthropic API key in the sidebar to continue.")
            return
        
        st.session_state.chat_started = True
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_claude_response(
                    st.session_state.messages,
                    st.session_state.api_key
                )
                st.markdown(response)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
