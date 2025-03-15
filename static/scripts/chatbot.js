document.addEventListener("DOMContentLoaded", function() {
    const chatInput = document.getElementById("chat-input");
    const chatButton = document.getElementById("send-button");
    const chatBox = document.getElementById("chat-box");

    chatButton.addEventListener("click", async function() {
        let userMessage = chatInput.value;
        chatBox.innerHTML += `<p><b>Tú:</b> ${userMessage}</p>`;
        chatInput.value = "";

        let response = await fetch("/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        });

        let data = await response.json();

        if (data.url) {
            window.location.href = data.url;  // Redirige a otra página
        } else {
            chatBox.innerHTML += `<p><b>Chatbot:</b> ${data.response}</p>`;
        }
    });
});
document.addEventListener("DOMContentLoaded", function() {
    const chatToggle = document.getElementById("chat-toggle");
    const chatContainer = document.getElementById("chat-container");
    const closeChat = document.getElementById("close-chat");
    const chatInput = document.getElementById("chat-input");
    const chatButton = document.getElementById("send-button");
    const chatBox = document.getElementById("chat-box");

    // Mostrar u ocultar chatbot
    chatToggle.addEventListener("click", () => chatContainer.classList.toggle("hidden"));
    closeChat.addEventListener("click", () => chatContainer.classList.add("hidden"));

    // Enviar mensaje al chatbot
    chatButton.addEventListener("click", async function() {
        let userMessage = chatInput.value.trim();
        if (userMessage === "") return;

        chatBox.innerHTML += `<p class="text-right"><b>Tú:</b> ${userMessage}</p>`;
        chatInput.value = "";

        let response = await fetch("/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        });

        let data = await response.json();

        if (data.url) {
            window.location.href = data.url;  // Redirige a otra página
        } else {
            chatBox.innerHTML += `<p class="text-left"><b>Chatbot:</b> ${data.response.text}</p>`;
        }

        chatBox.scrollTop = chatBox.scrollHeight; // Scroll automático
    });
});

