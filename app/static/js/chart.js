const socket = io();

const chatBox = document.getElementById("chat-box");
const msgInput = document.getElementById("msg");

socket.on("message", (msg) => {
  const div = document.createElement("div");
  div.textContent = msg;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
});

function sendMessage() {
  const msg = msgInput.value;
  if (msg.trim()) {
    socket.emit("message", msg);
    msgInput.value = "";
  }
}
