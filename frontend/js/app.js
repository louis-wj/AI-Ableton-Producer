const chat = document.getElementById('chat');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const activity = document.getElementById('activity');

function addMessage(text, isUser = false) {
    const msg = document.createElement('div');
    msg.className = `message ${isUser ? 'user-msg' : 'ai-msg'}`;
    msg.innerText = text;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

async function sendRequest() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, true);
    userInput.value = '';
    activity.innerText = "THINKING...";

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        addMessage(data.response);
        activity.innerText = data.idle ? "IDLE" : "EXECUTING";
        
    } catch (err) {
        addMessage("Connection Error. Ensure backend is running.");
        activity.innerText = "ERROR";
    }
}

sendBtn.onclick = sendRequest;
userInput.onkeydown = (e) => {
    if (e.key === 'Enter') sendRequest();
};
