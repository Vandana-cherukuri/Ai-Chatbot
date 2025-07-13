from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import markdown
import re
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize Gemini model - using the correct model name
model = genai.GenerativeModel('gemini-2.0-flash')

def process_markdown(text):
    """Convert markdown text to HTML with proper formatting"""
    # Configure markdown with extensions for better formatting
    md = markdown.Markdown(extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.nl2br'
    ])
    
    # Convert markdown to HTML
    html = md.convert(text)
    
    # Add custom CSS classes for better styling
    html = re.sub(r'<code>(?!<)', '<code class="inline-code">', html)
    html = re.sub(r'<pre><code>', '<pre><code class="code-block">', html)
    
    return html

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Get the user's message from the request
        if not request.json:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Check if API key is available
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'error': 'Gemini API key not configured. Please create a .env file with your GEMINI_API_KEY'}), 500
        
        # Check if API key looks valid (basic validation)
        if api_key == 'your_gemini_api_key_here' or len(api_key) < 20:
            return jsonify({'error': 'Invalid API key. Please check your .env file and ensure you have a valid Gemini API key'}), 500
        
        # Make API call to Gemini using the correct structure
        response = model.generate_content(
            user_message,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000,
                temperature=0.7
            )
        )
        
        # Extract the AI's response
        ai_response = response.text
        if ai_response is None:
            return jsonify({'error': 'No response from AI'}), 500
            
        ai_response = ai_response.strip()
        
        # Process markdown formatting
        formatted_response = process_markdown(ai_response)
        
        return jsonify({'response': formatted_response})
    
    except Exception as e:
        error_msg = str(e)
        print(f"Unexpected error: {error_msg}")
        
        # Check for specific Gemini error types
        if "quota" in error_msg.lower() or "quota_exceeded" in error_msg.lower():
            return jsonify({
                'error': 'API quota exceeded. Please check your Google AI Studio account.',
                'details': 'This usually means you\'ve hit your usage limits.'
            }), 429
        elif "invalid" in error_msg.lower() or "401" in error_msg.lower() or "403" in error_msg.lower():
            return jsonify({
                'error': 'Invalid API key. Please check your .env file and ensure you have a valid Gemini API key.',
                'details': 'Make sure your API key is correct and not expired.'
            }), 401
        elif "rate" in error_msg.lower():
            return jsonify({
                'error': 'Rate limit exceeded. Please wait a moment and try again.',
                'details': 'You\'re making too many requests too quickly.'
            }), 429
        elif "404" in error_msg.lower() or "not found" in error_msg.lower():
            return jsonify({
                'error': 'Model not found. Please check the model name.',
                'details': 'The specified model may not be available or may have changed.'
            }), 404
        else:
            return jsonify({
                'error': 'Something went wrong. Please try again.',
                'details': error_msg
            }), 500

if __name__ == '__main__':
    print("Starting Flask app on 127.0.0.1:5000")
    print("Debug mode: True")
    
    # Check if Gemini API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        if api_key == 'your_gemini_api_key_here' or len(api_key) < 20:
            print("✗ Invalid API key detected! Please check your .env file")
            print("   Make sure you've replaced 'your_gemini_api_key_here' with your actual Gemini API key")
        else:
            print("✓ Gemini API key found in environment variables")
            print(f"   Key starts with: {api_key[:8]}...")
    else:
        print("✗ Gemini API key not found! Please create a .env file with your GEMINI_API_KEY")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
    
    app.run(debug=True, host='127.0.0.1', port=5000)