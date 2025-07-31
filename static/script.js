document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    let conversationHistory = [];

    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(message, "user");
        userInput.value = "";

        conversationHistory.push({
            'role': 'user',
            'parts': [{ 'text': message }]
        });

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ history: conversationHistory }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const modelResponse = data.response;

            appendMessage(modelResponse, "model");
            conversationHistory.push({
                'role': 'model',
                'parts': [{ 'text': modelResponse }]
            });

        } catch (error) {
            console.error("Fetch error:", error);
            appendMessage(`Error: ${error.message}`, "error");
        }
    };

    const appendMessage = (message, sender) => {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});
