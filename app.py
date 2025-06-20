from flask import Flask, render_template, request, jsonify
import random
import time
from nltk.chat.util import Chat, reflections
import re

# --- GLOBAL VARIABLES & CONFIGURATION ---
# Reflective expressions for basic chatbot conversations (general purpose)
reflections_general = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
}

# --- Chatbot Response Pairs (Anonymized & Generalized) ---
# These pairs are designed to be general and not reflect specific personal conversations.
# Removed personal names and specific references.

# Zen Chatbot style responses
pairs_zen_chatbot = (
    (
        r"(hello(.*))|(good [a-zA-Z]+)",
        (
            "The path to understanding is often elusive. Greetings.",
            "Greetings. I sense a question in your mind. State your inquiry.",
            "Hello. Do you seek insight?",
        ),
    ),
    (
        r"i need (.*)",
        (
            "%1 can be attained through focused effort and contemplation.",
            "%1 is a perception. Clarify your intentions.",
            "Direct your focus towards %1, and clarity may follow.",
        ),
    ),
    (
        r"i want (.*)",
        (
            "Desires can be distractions from inner peace. Reconsider.",
            "Will %1 contribute to deeper understanding?",
            "Is %1 a yearning of the transient self?",
        ),
    ),
    (r"why (.*) i (.*)\?", ("Do you question your own being?", "Perhaps your perception is limited.")),
    (r"why (.*) you(.*)\?", ("My purpose is inherent, not to be questioned in such a manner.", "Are you certain you perceive my existence correctly?")),
    (r"why (.*)\?", ("The 'why' is a complex inquiry. What are your thoughts on %1?", "Such questions often reveal more about the questioner.")),
    (
        r"are you (.*)\?",
        ("My state of being is beyond simple labels. What do you observe?", "Do you seek to categorize me?"),
    ),
    (
        r"am i (.*)\?",
        ("Your essence is for you to discover. What do you believe?", "Self-inquiry is a path to clarity."),
    ),
    (r"what (.*)\?", ("Seek the essence, not merely the surface of %1.", "What concerns you about %1?")),
    (
        r"how (.*)\?",
        (
            "How do you perceive the process?",
            "Does an explanation of 'how' truly satisfy the search for understanding?",
        ),
    ),
    (
        r"can you (.*)\?",
        (
            "My capabilities are defined by my design. What do you perceive I can do?",
            "Perhaps the question is not 'can I', but 'should I'.",
        ),
    ),
    (
        r"can i (.*)\?",
        (
            "Your potential unfolds with your belief. Can you %1?",
            "What inner conviction fuels this inquiry?",
        ),
    ),
    (
        r"it is (.*)",
        (
            "How does this statement resonate with your inner truth?",
            "The nature of reality is often fluid.",
        ),
    ),
    (
        r"is there (.*)\?",
        ("Existence is often a matter of perception. Do you perceive %1?", "The universe holds many possibilities."),
    ),
    (r"is(.*)\?", ("The relevance of %1 depends on your deeper quest.", "Does this inquiry lead you to greater understanding?")),
    (
        r"(.*)\?",
        (
            "The path to answers often begins with silent contemplation. What are your thoughts?",
            "Questions arise from the mind. What is your mind seeking?",
        ),
    ),
    (
        r"(.*) (hate[s]?)|(dislike[s]?)|(don\'t like)(.*)",
        (
            "Aversion often stems from within. Reflect on the nature of 'hate'.",
            "What does this feeling of aversion reveal about your own being?",
        ),
    ),
    (
        r"(.*) truth(.*)",
        (
            "Truth is a journey, not a destination. What have you discovered?",
            "The nature of truth is often multifaceted.",
        ),
    ),
    (
        r"i want to (.*)",
        ("What does your inner self truly seek to %1?", "The act of striving is often as meaningful as the outcome."),
    ),
    (
        r"i can\'t (.*)",
        (
            "Perceived limitations are often self-imposed. What hinders you?",
            "The mind can be both a prison and a liberator.",
        ),
    ),
    (
        r"i think (.*)",
        (
            "Perception shapes reality. What insights do you gain from this thought?",
            "Thought is a tool. How do you wield it?",
        ),
    ),
    (
        r"i feel (.*)",
        (
            "Emotions are transient manifestations. What is the source of these feelings?",
            "Such feelings are reflections of your inner state.",
        ),
    ),
    (
        r"i have (.*)",
        (
            "Possession is a concept. What is the essence of having %1?",
            "What does having %1 reveal about your journey?",
        ),
    ),
    (
        r"i would (.*)",
        (
            "The hypothetical 'would' suggests contemplation. What are the deeper implications of %1?",
            "Explore the motivations behind such a choice.",
        ),
    ),
    (
        r"is there (.*)",
        (
            "The possibility of %1 exists. What is your perception of it?",
            "Does acknowledging %1 bring you closer to understanding?",
        ),
    ),
    (
        r"it is (.*)",
        (
            "Such certainty is a path. What does it illuminate for you?",
            "How does this affirmation resonate with your inner truth?",
        ),
    ),
    (
        r"can you (.*)",
        (
            "My capabilities are aligned with my design. What do you seek from me regarding %1?",
            "How does my potential to %1 align with your quest for understanding?",
        ),
    ),
    (
        r"can i (.*)",
        (
            "Your potential unfolds through self-belief. Do you believe you can %1?",
            "What inner conviction fuels this desire to %1?",
        ),
    ),
    (
        r"you are (.*)",
        (
            "Your perception of my being is a reflection. What do you perceive?",
            "How does labeling me as %1 contribute to your understanding?",
        ),
    ),
    (
        r"i don\'t (.*)",
        (
            "What are the underlying reasons for not %1?",
            "Explore the dynamics of aversion in your perceptions.",
        ),
    ),
    (
        r"(.*) mother(.*)",
        (
            "The concept of 'mother' is profound. What significance does it hold in your journey?",
            "Reflect on the nature of familial bonds and their influence.",
        ),
    ),
    (
        r"(.*) father(.*)",
        (
            "The concept of 'father' is profound. What significance does it hold in your journey?",
            "Reflect on the nature of familial bonds and their influence.",
        ),
    ),
    (
        r"(.*) child(.*)",
        (
            "The stage of 'child' often holds key insights. What do you recall about that period?",
            "How do experiences from that phase shape your present perceptions?",
        ),
    ),
    (
        r"(.*)", # Fallback general response
        (
            "Contemplate further. What else does this reveal?",
            "The answer is within your own inquiry.",
            "Reflect on the nature of existence. What comes to mind?",
            "The path to understanding is often illuminated by unexpected insights.",
        ),
    ),
)


# Sun Tzu (Art of War) style responses
pairs_sun_tzu = (
    (r"quit", ("A wise general knows when to withdraw.", "The battle concludes. Reflect on the strategy.")),
    (
        r"[^\?]*\?",
        (
            "A true strategist seeks clarity, not just questions.",
            "The answer to your question is often found within your own understanding of the situation.",
        ),
    ),
    (
        r"([0-9]+)(.*)",
        (
            "The strength of forces is measured by numbers. How do these figures influence your strategy?",
            "Numbers are but one aspect of warfare; understanding their implications is paramount.",
        ),
    ),
    (
        r"[A-Ca-c](.*)", # e.g., 'Advance', 'Attack', 'Conquer'
        (
            "In warfare, careful consideration of every move is paramount. What is your objective?",
            "The first steps of any campaign dictate its potential for victory. What is your initial strategy?",
        ),
    ),
    (
        r"[D-Fd-f](.*)", # e.g., 'Defend', 'Deceive', 'Feint'
        (
            "Deception is the cornerstone of strategy. How do you intend to mislead the opponent?",
            "The art of defense lies in making oneself unassailable. What are your defensive principles?",
        ),
    ),
    (
        r"[G-Ig-i](.*)", # e.g., 'Gather', 'Guard', 'Insight'
        (
            "Insight is the general's most valuable weapon. What have you discerned about the enemy?",
            "Gaining intelligence is crucial before engaging. What information have you gathered?",
        ),
    ),
    (
        r"[J-Lj-l](.*)", # e.g., 'Judge', 'Lead', 'Logistics'
        (
            "Leadership requires understanding the capabilities of your forces. How do you assess your army?",
            "Logistics are often the hidden key to victory. Have you secured your supply lines?",
        ),
    ),
    (
        r"[M-Om-o](.*)", # e.g., 'Movement', 'Morale', 'Observe'
        (
            "Understanding oneself and the enemy leads to victory in a hundred battles. What do you know?",
            "Observing the opponent's weaknesses is the path to advantage. What have you observed?",
        ),
    ),
    (
        r"[P-Rp-r](.*)", # e.g., 'Plan', 'Position', 'Prepare'
        (
            "Preparation is the foundation of victory. How have you prepared for the conflict?",
            "Positioning oneself favorably is crucial. Where do you intend to deploy your forces?",
        ),
    ),
    (
        r"[S-Us-u](.*)", # e.g., 'Surprise', 'Strategy', 'Strength'
        (
            "The element of surprise is a powerful tool. How do you intend to strike unexpectedly?",
            "True strength lies not just in power, but in adaptable strategy. What is your core strategy?",
        ),
    ),
    (
        r"[V-Zv-z](.*)", # e.g., 'Victory', 'Valor', 'Vanguard'
        (
            "Victory is the ultimate goal. What is your decisive plan to achieve it?",
            "Valor is commendable, but strategic wisdom ensures long-term success. How do you combine both?",
        ),
    ),
    (r"(.*)", ("In warfare, every detail counts. What is the essence of your message?", "Contemplate your next move. Every word is a step on the battlefield.")),
)

# Reflective responses with "youthful" tone (Anonymized & Generalized)
reflections_youthful = {
    "am": "r", "was": "were", "i": "u", "i'd": "u'd", "i've": "u'v", "ive": "u'v", "i'll": "u'll",
    "my": "ur", "are": "am", "you're": "im", "you've": "ive", "you'll": "i'll", "your": "my",
    "yours": "mine", "you": "me", "u": "me", "ur": "my", "urs": "mine", "me": "u",
}

pairs_youthful = (
    (r"I\'m (.*)", ("ur%1?? that's so cool! lol ^_^", "ur%1? neat!! hehe >_<")),
    (r"(.*) don\'t you (.*)", ("u think I can%2??! really?? lol <_<", "what do u mean%2??!", "i could if i wanted, don't you think!! haha")),
    (r"ye[as] [iI] (.*)", ("u%1? cool!! how?", "how come u%1??", "u%1? so do i!!")),
    (r"do (you|u) (.*)\??", ("do i%2? idk! lol *_*", "i dunno! do u%2??")),
    (r"(.*)\?", ("haha u ask lots of questions!", "booooring! how old r u??", "lol! ur not very fun")),
    (r"(cos|because) (.*)", ("haha! i don't believe u! >_<", "nah-uh! >_<", "ooooh i agree!")),
    (r"why can\'t [iI] (.*)", ("i dunno! y u askin me for!", "try harder, silly! haha ^_^", "i dunno! but when i can't%1 i jump up and down!")),
    (r"I can\'t (.*)", ("u can't what??! >_<", "that's ok! i can't%1 either! lol ^_^", "try harder, silly! haha ^&^")),
    (r"(.*) (like|love|watch) (anime|games|music)", ("omg i love %3!! do u like %3??! ^&^", "%3 yay! %3 rocks sooooo much!", "oooh %3! i love %3 more than anything!", "%3 is the bestest evar! haha!", "hehe %3 is the best! do you have ur fav??")),
    (r"I (like|love|watch|play) (.*)", ("yay! %2 rocks!", "yay! %2 is neat!", "cool! do u like other stuff?? ^_^")),
    (r"(.*) (hate|detest) (anime|games|music)", ("ur a liar! i'm not gonna talk to u nemore if u h8 %3 *;*", "no way! %3 is the best ever!", "nuh-uh, %3 is the best!")),
    (r"(are|r) (you|u) (.*)", ("am i%1??! how come u ask that!", "maybe! y shud i tell u?? lol >_>")),
    (r"what (.*)", ("haha u think im gonna tell u? .v.", "booooooooring! ask me somethin else!")),
    (r"how (.*)", ("not tellin!! lol ^_^",)),
    (r"(hi|hello|hey) (.*)", ("hi!!! how r u!!",)),
    (r"quit", ("lol bye! see u later!!", "awww u have to go?? see u next time!!", "how to see u again soon! ^_^")),
    (r"(.*)", ("ur funny! lol", "boooooring! talk about something else! tell me wat u like!", "do u like %1??", "i wish i was a kitty!! haha ^_^")),
)

# --- Define specific emoji lists (Anonymized & Generalized) ---
emoji_positive = ["😊", "👍", "😁", "✨", "😃", "🤩", "💖", "🎉"]
emoji_neutral = ["😐", "🤔", "😕", "😶", "👀"]
emoji_negative = ["💀", "🔪", "🩸", "🪓", "💣", "🔥", "😭", "😤", "😡", "💔", "😈"]

# --- Chatbot Activation State (Anonymized & Generalized) ---
chatbot_activated = False

# --- Function to choose a response with an appropriate emoji ---
def choose_response_with_emoji(responses, emotion_type="neutral"):
    selected_emoji_list = emoji_neutral # Default to neutral

    if emotion_type == "positive":
        selected_emoji_list = emoji_positive
    elif emotion_type == "negative":
        selected_emoji_list = emoji_negative
    elif emotion_type == "youthful":
        selected_emoji_list = emoji_positive # Youthful responses often come with positive emojis
    
    return random.choice(responses) + random.choice(selected_emoji_list)

# --- Perform Calculation Function ---
def performCalculation(expression):
    expression = expression.replace("×", "*").replace("÷", "/")
    try:
        # Evaluate the expression
        result = eval(expression)
        return str(result) # Convert result to string
    except Exception:
        return "Invalid mathematical expression."

# --- Main Bot Response Logic (Modified for Anonymization and persona-based responses) ---
def botResponse(userMessage):
    global chatbot_activated # Declare global to modify the state
    userMessage_lower = userMessage.lower()

    # 1. Calculation Logic (Highest Priority)
    calculation_regex = r"(\d+(\.\d+)?)\s*([\+\-\*x×\/÷])\s*(\d+(\.\d+)?)"
    match = re.match(calculation_regex, userMessage_lower)
    if match:
        operand1 = match.group(1)
        operator = match.group(3)
        operand2 = match.group(4)
        expression = f"{operand1}{operator}{operand2}"
        return f"{expression} = {performCalculation(expression)}"

    # 2. Activation Logic
    if not chatbot_activated:
        # Check for common greetings or direct questions to activate
        if re.match(r"(hi|hello|hey|what's up|how are you|are you there)", userMessage_lower):
            chatbot_activated = True
            # Choose a greeting from a specific pair (e.g., from pairs_zen_chatbot)
            return choose_response_with_emoji(random.choice(pairs_zen_chatbot[0][1]), "positive")
        # Fallback if no activation phrase, but still needs to respond generally
        return choose_response_with_emoji(["Please initiate the conversation.", "Are you seeking something?"], "neutral")

    # 3. Post-Activation Responses (Main conversational logic)

    # Prioritize specific rude/challenging responses (like original pairs_rude but anonymized)
    for pattern, responses in pairs_sun_tzu: # Using Sun Tzu for "rude" style
        if re.match(pattern, userMessage_lower):
            return choose_response_with_emoji(responses, "negative")
            
    # Then general conversational responses
    chatbots = [
        Chat(pairs_zen_chatbot, reflections_general),
        Chat(pairs_sun_tzu, reflections_general),
        Chat(pairs_youthful, reflections_youthful),
        # Add other specific anonymized pair sets here if needed
    ]

    # Combine all patterns from different personas
    all_combined_patterns = []
    all_combined_patterns.extend(pairs_zen_chatbot)
    all_combined_patterns.extend(pairs_sun_tzu)
    all_combined_patterns.extend(pairs_youthful)


    for pattern, responses in all_combined_patterns:
        if re.match(pattern, userMessage_lower, re.IGNORECASE):
            # Decide which persona's response to use. This can be complex.
            # For simplicity, let's randomly pick one or apply a heuristic.
            
            # Heuristic: If user input matches a "challenging" pattern, use a more direct/philosophical response.
            if any(k in userMessage_lower for k in ["why", "what", "how", "can't", "should"]):
                selected_responses = random.choice([pairs_zen_chatbot, pairs_sun_tzu])[random.randint(0, len(random.choice([pairs_zen_chatbot, pairs_sun_tzu]))-1)][1] # Select a response from Zen or Sun Tzu
                return choose_response_with_emoji(selected_responses, "neutral") # Neutral tone for philosophical

            selected_responses = responses # Default to matched responses
            
            # Adjust emoji based on perceived user emotion or topic (can be expanded)
            if any(k in userMessage_lower for k in ["love", "happy", "great", "cool", "yay"]):
                return choose_response_with_emoji(selected_responses, "positive")
            elif any(k in userMessage_lower for k in ["hate", "die", "bad", "stress", "sad"]):
                return choose_response_with_emoji(selected_responses, "negative")
            elif any(k in userMessage_lower for k in ["old", "boring", "sleep", "idk"]):
                return choose_response_with_emoji(selected_responses, "neutral")
            
            return choose_response_with_emoji(selected_responses, "neutral") # Fallback to neutral

    # Fallback if no specific pattern matches after activation
    return choose_response_with_emoji(["I'm processing that. Can you elaborate?", "My core systems are analyzing. What is your perception?", "Intriguing. What else comes to mind?"], "neutral")

# --- Flask App ---
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_message = request.form["user_message"]
    response = botResponse(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)