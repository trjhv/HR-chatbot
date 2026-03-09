# HR Assistant Chatbot 👔

A professional HR chatbot built with Streamlit and powered by Claude AI (Anthropic API).

## Features

- 💬 Interactive chat interface for HR inquiries
- 🎯 Pre-configured with common HR knowledge (PTO, benefits, 401k, holidays, etc.)
- 📚 Quick access to common questions
- 🔒 Secure API key handling
- 💾 Conversation history
- 📱 Responsive design

## Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com))

## Installation

1. **Clone or download the files**
   ```bash
   # Make sure you have app.py and requirements.txt
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key** (optional)
   
   You can either:
   - Enter it in the sidebar when running the app, OR
   - Set it as an environment variable:
   
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

## Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to that URL manually

3. **Enter your API key**
   - If you haven't set the environment variable, enter your API key in the sidebar

4. **Start chatting!**
   - Type your HR questions in the chat input
   - Or click one of the common questions in the sidebar

## Customization

### Update Company Information

Edit the `HR_KNOWLEDGE` variable in `app.py` to include your company's specific:
- Company name and contact information
- PTO policies
- Benefits details
- Holiday schedule
- Remote work policies
- Any other HR policies

### Modify the System Prompt

Update the `HR_SYSTEM_PROMPT` variable to:
- Change the chatbot's personality
- Add specific guidelines
- Include additional topics
- Adjust escalation procedures

### Add More Features

You can enhance the chatbot by:
- Adding file upload for employee handbooks
- Integrating with your HR database
- Adding authentication
- Implementing form submissions for PTO requests
- Adding analytics and usage tracking

## Common Questions Examples

- "How do I request time off?"
- "What are my health insurance options?"
- "How does the 401(k) matching work?"
- "What are the company holidays this year?"
- "What is the remote work policy?"
- "How do I enroll in benefits?"
- "When do I get my first paycheck?"

## Security Notes

⚠️ **Important Security Considerations:**

1. **API Key**: Never commit your API key to version control
2. **Sensitive Data**: Don't include actual employee data in the knowledge base
3. **Production Use**: For production, implement proper authentication and authorization
4. **Compliance**: Ensure compliance with data privacy regulations (GDPR, CCPA, etc.)

## Troubleshooting

**Issue**: "Authentication failed"
- **Solution**: Check that your API key is correct and valid

**Issue**: App doesn't start
- **Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Slow responses
- **Solution**: The Claude API may take a few seconds to respond, especially for longer conversations

## Cost Considerations

This chatbot uses the Claude Sonnet 4 model. Be aware of:
- API costs are based on token usage
- Each conversation incurs costs
- Monitor your usage at https://console.anthropic.com

## Support

For issues related to:
- **The chatbot code**: Check the code comments and customize as needed
- **Anthropic API**: Visit https://docs.anthropic.com
- **Streamlit**: Visit https://docs.streamlit.io

## License

This is a sample application. Customize and use as needed for your organization.

## Disclaimer

This chatbot is a tool to assist with common HR questions. It should not replace:
- Professional HR advice
- Legal counsel
- Official company policies
- Human judgment for sensitive matters

Always consult with your HR department for official guidance.
