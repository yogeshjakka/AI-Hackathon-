const chat = document.getElementById("chat");
const input = document.getElementById("input");
document.getElementById("send").onclick = async () => {
  const txt = input.value;
  if(!txt) return;
  const div = document.createElement("div"); div.className="msg user"; div.innerText = "You: "+txt;
  chat.appendChild(div);
  input.value="";
  const res = await fetch("http://localhost:8000/chat/message", {
    method:"POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({session_id:"s1", user_id:"user_1", message: txt, location: {"lat":12.97,"lon":77.59}})
  });
  const data = await res.json();
  const b = document.createElement("div"); b.className="msg bot"; b.innerText = "Bot: "+data.reply;
  chat.appendChild(b);
}
