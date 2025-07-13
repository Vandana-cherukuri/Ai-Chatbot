# AI Chatbot

A simple Flask-based AI chatbot that uses OpenAI's GPT-3.5-turbo model.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**
   - Copy `env_template.txt` to `.env`
   - Replace `your_openai_api_key_here` with your actual OpenAI API key
   - Get your API key from: https://platform.openai.com/api-keys

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Chatbot**
   - Open your browser and go to: http://127.0.0.1:5000

## Features

- Real-time chat interface
- Typing indicators
- Error handling
- Responsive design
- Modern UI with animations

## Recent Fixes Applied

- ✅ Fixed DOM element ID mismatch between HTML and JavaScript
- ✅ Added missing click event listener for send button
- ✅ Updated OpenAI API usage to current client-based approach
- ✅ Updated openai package to latest version (1.3.0)
- ✅ Added proper API key validation
- ✅ Created environment variable template

## Requirements

- Python 3.7+
- OpenAI API key
- Flask
- OpenAI Python library 