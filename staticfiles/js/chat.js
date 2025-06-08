// ========== Scroll to Bottom ==========
function scrollToBottom() {
    const chatContainer = document.getElementById("messages-container");
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// ========== Check if Current Page is a Chat Page ==========
function isOnChatPage() {
    const path = window.location.pathname;
    const result = /^\/chat-user\/\d+\/?$/.test(path) || /^\/chat-super\/\d+\/?$/.test(path);
    return result;
}

console.log(isOnChatPage());
console.log(window.location.pathname);

// ========== Notification Sound ==========
const notifysound = new Audio('/static/audio/notify.mp3');

// ========== Get Current User Info ==========
const userDataElement = document.getElementById("user-data");

// ========== Chat WebSocket ==========
if (userDataElement) {
    const currentUser = JSON.parse(userDataElement.textContent);

    if (isOnChatPage()) {
        console.log("On chat-page:", window.location.pathname);
        const roomNumber = JSON.parse(document.getElementById('room-data').textContent);
        const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat-user/' + roomNumber + '/');

        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            if (data.message) {
                const messageBox = document.createElement("p");
                messageBox.textContent = `${data.message} ${data.timestamp}`;

                if (data.sender === currentUser.username) {
                    messageBox.className = "p-2 bg-blue-400 text-white self-end rounded-xl border w-fit";
                } else {
                    messageBox.className = "p-2 bg-gray-400 rounded-xl self-start border w-fit flash";
                }

                document.getElementById("messages-container").appendChild(messageBox);
                scrollToBottom();

                setTimeout(() => {
                    messageBox.classList.remove("flash");
                }, 1000);
            }
        };

        // ========== Send Message ==========
        document.getElementById("chat-form").addEventListener("submit", function (e) {
            e.preventDefault();
            const input = document.getElementById("message-input");
            const message = input.value.trim();

            if (message !== "") {
                chatSocket.send(JSON.stringify({ message }));
                input.value = "";
            }
        });
    }

    // ========== Notify WebSocket (Only on non-chat pages) ==========
    if (!isOnChatPage()) {
        console.log("Not in the chat page, the current path is:", window.location.pathname);
        const notifySocket = new WebSocket('ws://' + window.location.host + '/ws/notify/');
        console.log(notifySocket);

        notifySocket.onmessage = function (e) {
            const data = JSON.parse(e.data);

            if (data.type === "unread_count") {
                let notifyId;

                if (currentUser.is_superuser || currentUser.role === "super") {
                    notifyId = data.sender === currentUser.username ? "messages-notify" : "chats-notify";
                } else {
                    notifyId = data.sender === currentUser.username ? "chats-notify" : "messages-notify";
                }

                updateNotifyBubble(notifyId, data.count);

                if (data.count > 0) {
                    notifysound.play();
                    incrementNotify(notifyId);
                }
            }
        };
    }
}

// ========== Increase Notification Count ==========
function incrementNotify(id) {
    const bubble = document.getElementById(id);
    if (bubble) {
        let count = parseInt(bubble.textContent) || 0;
        bubble.textContent = count + 1;
        bubble.classList.remove("hidden");
    }
}

// ========== Set or Hide Notification Count ==========
function updateNotifyBubble(id, count) {
    const bubble = document.getElementById(id);
    if (bubble) {
        if (count > 0) {
            bubble.textContent = count;
            bubble.classList.remove("hidden");
        } else {
            bubble.textContent = 0;
            bubble.classList.add("hidden");
        }
    }
}

// ========== Reset on Page Load ==========
window.onload = function () {
    scrollToBottom();
    if (isOnChatPage()) {
        updateNotifyBubble("messages-notify", 0);
    }
}