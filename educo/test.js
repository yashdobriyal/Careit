// Show a greeting message when the chatbot starts
function showGreetingMessage() {
    const chatBox = document.getElementById("chat-box");
    const greetingMessage = "Hello! My name is Careit, I'm here to help. Select a question or type your own.";
    const messageElement = document.createElement("div");
    messageElement.className = "bot-message";
    messageElement.textContent = greetingMessage;
    chatBox.appendChild(messageElement);
}

// Send user message
function sendMessage() {
    const userInput = document.getElementById("user-input");
    const message = userInput.value;
    userInput.value = "";  // Clear input box
    displayMessage(message, "user-message");

    fetch('http://127.0.0.1:5000/chat', {  // Updated URL
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => displayMessage(data.reply, "bot-message"))
    .catch(error => displayMessage("Error: Unable to send message", "bot-message"));
}

function sendPredefinedMessage(message) {
    displayMessage(message, "user-message");

    fetch('http://127.0.0.1:5000/chat', {  // Updated URL
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => displayMessage(data.reply, "bot-message"))
    .catch(error => displayMessage("Error: Unable to send message", "bot-message"));
}

// Display message in chat box
function displayMessage(message, className) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("div");
    const tag = document.createElement("strong");

    // Set tag text based on message type
    if (className === "user-message") {
        tag.textContent = "User: ";
    } else {
        tag.textContent = "Careit: ";
    }

    // Add tag and message content
    messageElement.className = className;
    messageElement.appendChild(tag);
    messageElement.appendChild(document.createTextNode(message));

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto scroll to bottom
}
