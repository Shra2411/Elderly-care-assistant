// Toggle chatbot visibility
const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbotBox = document.getElementById('chatbot-box');

chatbotToggle.addEventListener('click', () => {
    if (chatbotBox.style.display === 'none') {
        chatbotBox.style.display = 'flex';
    } else {
        chatbotBox.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', () => {

    // ------------------- Fetch Health Tips -------------------
    document.getElementById("fetchHealthTips").addEventListener("click", () => {
        const tips = [
            "Stay hydrated by drinking plenty of water.",
            "Engage in regular physical activity.",
            "Maintain a balanced diet rich in fruits and vegetables.",
            "Get enough sleep and rest.",
            "Stay socially active to combat isolation."
        ];

        const tipsContainer = document.getElementById("healthTipsResponse");
        tipsContainer.innerHTML = ""; // clear previous tips

        tips.forEach(tip => {
            const li = document.createElement("li");
            li.textContent = tip;
            tipsContainer.appendChild(li);
        });
    });

    // ------------------- Submit Health Data -------------------
    document.getElementById('healthDataForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const healthCondition = document.getElementById('healthCondition').value;
        const medication = document.getElementById('medication').value;

        fetch('/health-data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ healthCondition, medication })
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('healthDataResponse').innerText = data.message;
                document.getElementById('healthDataForm').reset();
            })
            .catch(error => {
                document.getElementById('healthDataResponse').innerText =
                    'Error submitting health data: ' + error.message;
            });
    });

    // ------------------- Voice Command Feature -------------------
    const startVoiceBtn = document.getElementById('startVoiceCommand');
    if (startVoiceBtn) {
        startVoiceBtn.addEventListener('click', function () {
            if (!('webkitSpeechRecognition' in window)) {
                document.getElementById('voiceCommandResult').innerText =
                    'Your browser does not support voice recognition.';
                return;
            }

            const recognition = new webkitSpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.start();
            document.getElementById('voiceCommandResult').innerText = "Listening... Speak now.";

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('voiceCommandResult').innerText = `You said: ${transcript}`;

                fetch('/process-voice', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: transcript })
                })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('voiceCommandResult').innerText += `\nAssistant: ${data.response}`;

                        const utterance = new SpeechSynthesisUtterance(data.response);
                        utterance.lang = 'en-US';
                        window.speechSynthesis.speak(utterance);
                    })
                    .catch(error => {
                        document.getElementById('voiceCommandResult').innerText += '\nError: ' + error.message;
                    });
            };

            recognition.onerror = (error) => {
                document.getElementById('voiceCommandResult').innerText = 'Error: ' + error.error;
            };
        });
    }

    // ------------------- Chatbot -------------------
    const chatbox = document.getElementById('chatbox');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');

    if (chatbox && chatInput && sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') sendMessage();
        });
    }

    function appendMessage(sender, message) {
        const p = document.createElement('p');
        p.className = sender;
        p.innerHTML = `<b>${sender === 'user' ? 'You' : 'Bot'}:</b> ${message}`;
        chatbox.appendChild(p);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        appendMessage('user', message);
        chatInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            appendMessage('bot', data.reply);
        } catch (error) {
            appendMessage('bot', 'Error connecting to server.');
            console.error(error);
        }
    }

});
