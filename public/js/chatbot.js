(function () {
    const API_URL = "http://localhost:8000/ask"; // 👉 change in production
    // const BoatName = "ModernTech Academy Chat";
    const BoatName = "Ranjit's HelpLine";

    // Create chatbot button
    const button = document.createElement("div");
    button.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="white" viewBox="0 0 24 24">
    <path d="M2 2h20v14H6l-4 4V2z"/>
    </svg>
    `;
    button.style.position = "fixed";
    button.style.bottom = "20px";
    button.style.right = "20px";
    button.style.width = "60px";
    button.style.height = "60px";
    button.style.background = "#007bff";
    button.style.color = "#fff";
    button.style.borderRadius = "50%";
    button.style.display = "flex";
    button.style.alignItems = "center";
    button.style.justifyContent = "center";
    button.style.cursor = "pointer";
    button.style.zIndex = "9999";
    document.body.appendChild(button);

    // Chat container
    const chatBox = document.createElement("div");
    chatBox.style.position = "fixed";
    chatBox.style.bottom = "90px";
    chatBox.style.right = "20px";
    chatBox.style.width = "300px";
    chatBox.style.height = "400px";
    chatBox.style.background = "#fff";
    chatBox.style.border = "1px solid #ccc";
    chatBox.style.borderRadius = "10px";
    chatBox.style.display = "none";
    chatBox.style.flexDirection = "column";
    chatBox.style.zIndex = "9999";

    chatBox.innerHTML = `
    <div style="background:#007bff;color:#fff;padding:10px;border-radius:10px 10px 0 0;">
      ${BoatName}
    </div>
    <div id="chat-messages" style="flex:1;padding:10px;overflow:auto;"></div>
    <div style="display:flex;">
      <input id="chat-input" style="flex:1;padding:10px;border:none;border-top:1px solid #ccc;" placeholder="Ask something..." />
      <button id="send-btn" style="padding:10px;background:#007bff;color:#fff;border:none;">Send</button>
    </div>
  `;

    document.body.appendChild(chatBox);

    // Toggle chat
    button.onclick = () => {
        chatBox.style.display = chatBox.style.display === "none" ? "flex" : "none";
    };

    // Send message
    async function sendMessage() {
        const input = document.getElementById("chat-input");
        const messages = document.getElementById("chat-messages");

        const userText = input.value;
        if (!userText) return;

        messages.innerHTML += `<div><b>You:</b> ${userText}</div>`;
        input.value = "";

        const res = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: userText })
        });

        const data = await res.json();

        messages.innerHTML += `<div><b>Bot:</b> ${data.answer}</div>`;
        messages.scrollTop = messages.scrollHeight;
    }

    document.addEventListener("click", function (e) {
        if (e.target && e.target.id === "send-btn") {
            sendMessage();
        }
    });

    document.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
})();