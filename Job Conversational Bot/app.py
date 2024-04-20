from flask import Flask, render_template, request
from rasa.core.agent import Agent
from rasa.core.channels.socketio import SocketIOInput

app = Flask(__name__)
agent = Agent.load('path/to/your/rasa/model')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Process user input and return the agent's response.

    Args:
        user_input (str): The user's input message.

    Returns:
        str: The text of the agent's response.
    """
    user_input = request.form['user_input']
    response = agent.handle_text(user_input)
    return response[0]['text']

if __name__ == '__main__':
    input_channel = SocketIOInput(
        socket_app=app,
        cors_allowed=True,
        socket_path='/socket.io',
        socket_host='localhost',
        socket_port=5005
    )

    agent.handle_channels([input_channel], 5005, cors_allowed=True)