import streamlit as st
import anthropic
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="HR Assistant Chatbot",
    page_icon="👔",
    layout="wide"
)

# HR System Prompt
HR_SYSTEM_PROMPT = """You are a helpful and professional HR assistant chatbot for a company. Your role is to:

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

Remember: You are a helpful assistant, not a replacement for human HR professionals. Complex or sensitive matters should be escalated to the HR department.
"""

# Sample HR Knowledge Base (you can expand this)
HR_KNOWLEDGE = """
COMPANY INFORMATION:
- Company Name: Acme Corporation
- HR Email: hr@acmecorp.com
- HR Phone: (555) 123-4567
- HR Office Hours: Monday-Friday, 9 AM - 5 PM EST

PTO POLICY:
- New employees: 15 days per year
- Employees with 3+ years: 20 days per year
- Employees with 5+ years: 25 days per year
- PTO requests should be submitted at least 2 weeks in advance
- Submit requests through the HR portal or email hr@acmecorp.com

HEALTH INSURANCE:
- Coverage begins first day of the month following hire date
- Three plan options: Basic, Standard, Premium
- Open enrollment: November 1-30 each year
- Dependents can be added during open enrollment or within 30 days of qualifying life event

401(k) PLAN:
- Eligible after 90 days of employment
- Company matches 50% of contributions up to 6% of salary
- Immediate vesting of employee contributions
- Company match vests over 3 years

HOLIDAYS:
- New Year's Day
- Memorial Day
- Independence Day
- Labor Day
- Thanksgiving (2 days)
- Christmas Day
- Plus 2 floating holidays per year

REMOTE WORK:
- Hybrid policy: 2-3 days in office per week
- Full remote available for approved roles
- Remote work agreement required
- Home office stipend: $500/year
"""

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY", "")

def get_claude_response(messages, api_key):
    """Get response from Claude API"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Prepare messages with system context
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

def main():
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "Anthropic API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your Anthropic API key. Get one at https://console.anthropic.com"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your API key to use the chatbot")
        
        st.divider()
        
        # Quick links
        st.subheader("📚 Quick Resources")
        st.markdown("""
        - [HR Portal](#)
        - [Benefits Guide](#)
        - [Employee Handbook](#)
        - [Submit PTO Request](#)
        - [Contact HR](mailto:hr@acmecorp.com)
        """)
        
        st.divider()
        
        # Common questions
        st.subheader("💡 Common Questions")
        common_questions = [
            "How do I request time off?",
            "What are the health insurance options?",
            "How does the 401(k) matching work?",
            "What are the company holidays?",
            "What is the remote work policy?"
        ]
        
        for question in common_questions:
            if st.button(question, use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })
                st.rerun()
        
        st.divider()
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Main content
    st.title("👔 HR Assistant Chatbot")
    st.markdown("Welcome! I'm here to help answer your HR-related questions.")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about HR policies, benefits, or procedures..."):
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your Anthropic API key in the sidebar to continue.")
            return
        
        # Add user message to chat
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
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
