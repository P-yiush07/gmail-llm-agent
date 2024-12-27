from phi.agent import Agent
from phi.model.google import Gemini
from dotenv import load_dotenv
from email_tools import send_email
import os

load_dotenv()

# Create a Gemini wrapper around your model
gemini_model = Gemini(
    model_name="gemini-1.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY")
)

def clean_email_body(text: str) -> str:
    """Clean up email body by replacing escape characters with actual line breaks"""
    # First replace any \\ with \
    text = text.replace('\\\\', '\\')
    # Then replace \n with actual newlines
    text = text.replace('\\n', '\n')
    # Finally replace any remaining \ at the end of lines
    text = text.replace('\\\n', '\n')
    # Remove any standalone \ characters
    text = text.replace('\\', '')
    return text

def draft_email(to_email: str, subject: str, body: str) -> str:
    """Draft an email and return the formatted preview"""
    cleaned_body = clean_email_body(body)
    preview = f"""
To: {to_email}
Subject: {subject}

{cleaned_body}
"""
    return preview

def send_formatted_email(to_email: str, subject: str, body: str) -> str:
    """Send an email with properly formatted body text"""
    return send_email(to_email, subject, clean_email_body(body))

agent = Agent(
    description="You are an email agent that can draft and send emails. You always write detailed, warm, and engaging emails.",
    model=gemini_model,
    tools=[draft_email, send_formatted_email],
    show_tool_calls=True,
    markdown=True,
    add_history_to_messages=True,
    num_history_responses=2,
    instructions=[
        "For [your name] use Nuke",
        "Always draft the email first using draft_email tool",
        "After showing the draft, ask for user confirmation before sending",
        "Only send the email using send_formatted_email when user confirms",
        "When writing emails:",
        "- Include a warm and friendly greeting",
        "- Write multiple paragraphs with relevant details",
        "- Show genuine interest in the recipient's situation",
        "- Add context-appropriate questions",
        "- Close with a warm sign-off",
        "- Keep a professional yet friendly tone throughout"
    ]
)

# Function to get user confirmation
def get_user_confirmation() -> str:
    while True:
        print("\nWhat would you like to do with this email?")
        print("1. Send the email as is (yes/y)")
        print("2. Make it shorter (shorter/s)")
        print("3. Make it longer (longer/l)")
        print("4. Change the tone (tone/t)")
        print("5. Don't send and start over (no/n)")
        
        response = input("\nYour choice: ").lower()
        
        if response in ['yes', 'y', '1']:
            return "send"
        elif response in ['shorter', 's', '2']:
            return "shorter"
        elif response in ['longer', 'l', '3']:
            return "longer"
        elif response in ['tone', 't', '4']:
            return "tone"
        elif response in ['no', 'n', '5']:
            return "cancel"
        print("Please select a valid option")

# Modified workflow with enhanced confirmation
initial_prompt = "Write a email to webdevpiyush.07@gmail.com congratulating him on his new bike, for subject use 'congrats'"
response = agent.print_response(initial_prompt)

while True:
    user_choice = get_user_confirmation()
    if user_choice == "send":
        agent.print_response("Please send the email you just drafted")
        break  # Exit the loop after sending
    elif user_choice == "shorter":
        response = agent.print_response("Please make the previous email shorter while keeping the main points")
    elif user_choice == "longer":
        response = agent.print_response("Please make the previous email longer with more details and warmth")
    elif user_choice == "tone":
        tone_choice = input("\nWhat tone would you prefer? (formal/casual/excited): ")
        response = agent.print_response(f"Please rewrite the previous email in a {tone_choice} tone")
    else:  # cancel
        agent.print_response("Don't send the email")
        break  # Exit the loop if cancelled
