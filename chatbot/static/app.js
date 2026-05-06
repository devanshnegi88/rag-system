async function sendQuery() {

    const input = document.getElementById("query");

    const query = input.value;

    if (!query) return;

    addMessage(query, "user");

    input.value = "";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                query: query
            })

        });

        const data = await response.json();

        addMessage(
            data.response,
            "bot"
        );

    } catch (error) {

        addMessage(
            "Error connecting to server.",
            "bot"
        );

        console.error(error);
    }
}

function addMessage(text, sender) {

    const box = document.getElementById("chat-box");

    const div = document.createElement("div");

    div.classList.add("message");
    div.classList.add(sender);

    div.innerText = text;

    box.appendChild(div);

    box.scrollTop = box.scrollHeight;
}