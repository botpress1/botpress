import streamlit as st
import requests

# Set up the Streamlit layout
st.title("Fitness Chatbot")
st.write("Welcome to the fitness chatbot! Type your queries below to interact.")

# Initialize session state to store conversation history and conversation ID
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = None

# Function to create a new conversation with the Botpress chatbot API
def create_conversation():
    botpress_url = "https://api.botpress.cloud/v1/chat/conversations"
    headers = {
        "Authorization": f"Bearer bp_pat_0v0jBxfBlOrKvuSR9WPKbteAb0izCCe3MnmV",
        "x-bot-id": "c3ab3510-aaaf-409b-ae6e-c4d752b80ab6",
        "Content-Type": "application/json"
    }
    # Modify the payload to include 'integrationName' as required by the Botpress API
    payload = {
        "channel": "api",
        "Webchat": "a2c53580-3365-4b85-83e1-ac313a9916b1",  # Specify the integration name
        "tags": {
            "category": "fitness",
            "platform": "streamlit"
        }
    }

    try:
        response = requests.post(botpress_url, json=payload, headers=headers)
        response_data = response.json()
        print("Conversation created with ID:", response_data)  # Print the conversation ID for debugging
        return response_data["id"]  # Return the conversation ID
    except Exception as e:
        st.error(f"Error creating conversation: {e}")
        print(response.json())  # Print full response for debugging
        return None

# Function to send a message to the Botpress chatbot API and get a response
def send_message_to_botpress(message, conversation_id):
    botpress_url = f"https://api.botpress.cloud/v1/chat/conversations/{conversation_id}/messages"
    payload = {"type": "text", "text": message}
    headers = {
        "Authorization": f"Bearer bp_pat_0v0jBxfBlOrKvuSR9WPKbteAb0izCCe3MnmV",
        "x-bot-id": "c3ab3510-aaaf-409b-ae6e-c4d752b80ab6",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(botpress_url, json=payload, headers=headers)
        response_data = response.json()
        # Extract bot's response text
        if 'responses' in response_data and len(response_data['responses']) > 0:
            return response_data['responses'][0]['text']
        else:
            return "Sorry, I didn't understand that."
    except Exception as e:
        st.error(f"Error sending message: {e}")
        return "Sorry, I'm having trouble connecting to the chatbot server."

# Function to handle form submission
def submit_message():
    # Create a new conversation if it doesn't exist
    if not st.session_state.conversation_id:
        st.session_state.conversation_id = create_conversation()
    
    # Proceed only if the conversation ID was successfully created
    if st.session_state.conversation_id:
        # Add user's message to the session state
        st.session_state.messages.append({"sender": "user", "text": st.session_state.user_input})

        # Get bot's response
        bot_response = send_message_to_botpress(st.session_state.user_input, st.session_state.conversation_id)
        st.session_state.messages.append({"sender": "bot", "text": bot_response})

        # Clear the input box after submission
        st.session_state.user_input = ""

# Input box for the user's message with a callback
st.text_input("Your Message:", key="user_input", on_change=submit_message)

# Display the conversation history
for index, message in enumerate(st.session_state.messages):
    if message["sender"] == "user":
        st.text_area("You", value=message["text"], key=f"user_{index}", height=50, disabled=True)
    else:
        st.text_area("Bot", value=message["text"], key=f"bot_{index}", height=50, disabled=True)
