// ==========================
// 📦 Chat App JavaScript
// ==========================

// 🔄 Auto Scroll to Bottom
function scrollToBottom() {
    const chatContainer = document.getElementById("messages-container");
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

window.onload = scrollToBottom;

// 📤 WebSocket Connection
const notifysound = new Audio('/static/audio/notify.mp3');
const roomNumber = JSON.parse(document.getElementById('room-data').textContent);
const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat-user/' + roomNumber + '/');
const currentUser = JSON.parse(document.getElementById("user-data").textContent);

// 📤 Send Message
document.getElementById("chat-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const input = document.getElementById("message-input");
    const message = input.value.trim();

    if (message !== "") {
        chatSocket.send(JSON.stringify({ "message": message }));
        input.value = "";
    }
});

// 📥 Receive Message
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const sender = data.sender;
    const timestamp = data.timestamp;

    const messageBox = document.createElement("p");
    messageBox.textContent = message + " " + timestamp;

    if (sender === currentUser) {
        messageBox.className = "p-2 bg-blue-400 text-white self-end rounded-xl border w-fit";
        
    } else {
        messageBox.className = "p-2 bg-gray-400 rounded-xl self-start border w-fit flash";
    }
    
    const container = document.getElementById("messages-container");
    container.appendChild(messageBox);
    if (sender !== currentUser) {
        notifysound.play();
    }
    

    scrollToBottom();

    setTimeout(() => {
        messageBox.classList.remove("flash");
    }, 1000);

    handleNotification(sender);
};

// 🔔 Handle Notification (Fixed and smart)
function handleNotification(sender) {
    const isOnMessagesPage = window.location.pathname.includes('/chat-user/');
    const isonsuperpage = window.location.pathname.includes('/chat-super/');
    const messagesNotify = document.getElementById("messages-notify");
    const chatsNotify = document.getElementById("chats-notify");

    if (!isonsuperpage && !isOnMessagesPage && sender !== currentUser) {
        // 📢 Only trigger if NOT on chat page AND sender is NOT current user
        if (messagesNotify) {
            messagesNotify.classList.remove("hidden");  
            let count = parseInt(messagesNotify.textContent) || 0;
            messagesNotify.textContent = count + 1;
        }
        if (chatsNotify) {
            chatsNotify.classList.remove("hidden");
            let count = parseInt(chatsNotify.textContent) || 0;
            chatsNotify.textContent = count + 1;
        }
         
    }
}

// 🧹 Reset Notification Bubbles
function resetNotification(id) {
    const btn = document.getElementById(id + "-btn");
    const notify = document.getElementById(id + "-notify");

    if (btn && notify) {
        btn.addEventListener("click", () => {
            notify.textContent = 0;
            notify.classList.add("hidden");
        });
    }
}

resetNotification("messages");
resetNotification("chats");
