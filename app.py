from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Sample health tips
health_tips = [
    "Stay hydrated by drinking plenty of water.",
    "Engage in regular physical activity.",
    "Maintain a balanced diet rich in fruits and vegetables.",
    "Get enough sleep and rest.",
    "Stay socially active to combat isolation."
]

# Store health data (in-memory for simplicity)
health_data = []


# ---------- Routes for Pages ----------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/voice-command')
def voice_command():
    return render_template('voice-command.html')


@app.route('/medication-reminder')
def medication_reminder():
    return render_template('medication-reminder.html')


@app.route('/schedule-appointment')
def schedule_appointment():
    return render_template('schedule-appointment.html')


@app.route('/emergency-help')
def emergency_help():
    return render_template('emergency-help.html')


# ---------- API Routes ----------
@app.route('/health-tips', methods=['GET'])
def get_health_tips():
    return jsonify(health_tips)


@app.route('/health-data', methods=['POST'])
def submit_health_data():
    data = request.json
    health_data.append(data)
    return jsonify({"message": "Health data submitted successfully!"})


@app.route('/process-voice', methods=['POST'])
def process_voice():
    data = request.json
    command = data.get('command', '').lower()

    response_message = ""

    if any(word in command for word in ["health", "tip", "tips", "advice", "wellness", "exercise", "diet"]):
        response_message = (
            "Here are some health tips: Stay hydrated, exercise regularly, "
            "eat a balanced diet rich in fruits and vegetables, and get enough rest."
        )
    elif any(word in command for word in ["emergency", "help", "doctor", "ambulance", "urgent", "accident"]):
        response_message = "Contacting emergency services immediately..."
    elif any(word in command for word in ["medicine", "medication", "reminder", "pill", "dose", "take medicine"]):
        response_message = "Sure, I will remind you to take your medication at the scheduled time."
    elif any(word in command for word in ["appointment", "schedule", "doctor visit", "booking", "consultation"]):
        response_message = "Okay, let's schedule a doctor’s appointment at your preferred date and time."
    elif any(word in command for word in ["sleep", "rest", "nap", "relax"]):
        response_message = "Remember to get adequate sleep and take short breaks to stay healthy."
    elif any(word in command for word in ["social", "chat", "call family", "friends"]):
        response_message = "Try to stay socially active. You can call or message your friends and family."
    elif any(word in command for word in ["water", "hydrate", "drink"]):
        response_message = "Don't forget to drink enough water throughout the day."
    else:
        response_message = "I didn't understand the command. Please try again."

    return jsonify({"response": response_message})

# ---------- Chatbot Route ----------
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").lower()

    # Simple rule-based responses
    responses = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! How are you feeling today?",
    "medication": "You should take your medication on time. Do you want me to set a reminder?",
    "appointment": "You can schedule an appointment from the 'Schedule Appointment' tab.",
    "voice": "You can use the Voice Command tab to give instructions verbally.",
    "emergency": "For emergencies, please use the Emergency Help tab immediately.",
    "health tips": "Here are some health tips: Stay hydrated, exercise regularly, eat a balanced diet, and get enough rest.",
    
    # Common illness/symptoms
    "fever": "If you have a fever, rest, stay hydrated, and monitor your temperature. See a doctor if it exceeds 102°F or persists.",
    "cold": "For a cold, drink warm fluids, rest, and consider over-the-counter remedies if needed.",
    "cough": "For a mild cough, try honey, warm fluids, and rest. See a doctor if persistent or severe.",
    "headache": "Rest in a quiet room, stay hydrated, and consult a doctor if headaches are frequent or severe.",
    "stomach": "Avoid heavy/spicy foods, stay hydrated, and consult a doctor if pain persists.",
    
    # Chronic / serious conditions
    "diabetes": "Maintain a balanced diet, monitor blood sugar, and take prescribed medications. Regular check-ups are important.",
    "hypertension": "Reduce salt intake, exercise moderately, take prescribed medication, and monitor blood pressure regularly.",
    "heart attack": "If you suspect a heart attack, call emergency services immediately. Do not drive yourself.",
    "stroke": "If you notice sudden weakness, slurred speech, or facial droop, call emergency services immediately.",
    "heart": "For heart-related issues, avoid strenuous activity, take prescribed medications, and monitor symptoms closely.",
    "kidney": "For kidney problems, follow your doctor's advice, maintain hydration, and monitor diet carefully.",
    "liver": "For liver issues, avoid alcohol, follow prescribed medication, and consult your doctor regularly.",
    "cancer": "For cancer or suspected symptoms, consult your oncologist immediately and follow medical guidance.",
    "asthma": "Use your inhaler as prescribed, avoid triggers, and seek medical help during severe attacks.",
    "arthritis": "Regular movement, physical therapy, and medications can help manage arthritis. Consult your doctor for severe pain.",
    "alzheimers": "Ensure a safe environment, engage in memory activities, and follow medical guidance. Consult specialists as needed.",
    "parkinsons": "Follow prescribed medications, physical therapy, and regular doctor check-ups for symptom management.",
    "mental health": "For anxiety, depression, or other mental health concerns, seek professional help. Support from family is important.",
    
    "allergy": "Avoid triggers, consider antihistamines, and consult a doctor for severe reactions.",
    "cold and flu": "Rest, drink fluids, and consider over-the-counter meds. Seek attention if symptoms worsen.",
    
    "default": "Sorry, I didn't understand that. Please try asking differently or consult a doctor for serious issues."
}


    # Check if any keyword matches
    for key in responses:
        if key in user_input:
            return jsonify({"reply": responses[key]})

    return jsonify({"reply": responses["default"]})



if __name__ == '__main__':
    app.run(debug=True)
