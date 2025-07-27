import google.generativeai as genai

# turn this on if you're just testing stuff (no Gemini calls)
MOCK_MODE = False  # Set to False when you're ready to demo with Gemini

if not MOCK_MODE:
    genai.configure(api_key="INSERT YOUR API KEY HERE")
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")


def set_question_difficulty(prompt_level="easy"):
    prompt_map = {
        "easy": "on a general knowledge topic for beginners.",
        "medium": "that requires some critical thinking or background knowledge.",
        "hard": "that is challenging and requires higher-level reasoning."
    }
    return prompt_map.get(prompt_level, prompt_map["easy"])


def generate_quiz_question(topic, difficulty="easy", recent_questions=None):
    if MOCK_MODE:
        return {
            'question': f"What is a basic concept in {topic}?",
            'choices': ["Option A", "Option B", "Option C", "Option D"],
            'answer': "Option A",
            'explanation': f"This is a sample explanation related to {topic}.",
            'difficulty': 'easy',
            'question_text': f"What is a basic concept in {topic}?"
        }

    if not topic:
        raise ValueError("Topic is required to generate a quiz question.")

    difficulty_prompt = set_question_difficulty(difficulty)
    recent_qs = list(recent_questions)[-3:] if recent_questions else []
    prompt = f"""
You are an expert tutor. Generate one unique multiple-choice quiz question on the topic: "{topic}"

Requirements:
- Ask a clear, academically accurate question.
- Provide four answer options labeled A, B, C, and D.
- Only one answer should be correct.
- Clearly label the correct answer with: Answer: [Correct Letter]
- Also include a brief explanation after the answer, clearly labeled: Explanation: [your explanation here]
- Do not repeat any recent questions that begin with: {{recent_questions}}

Example:
What does CPU stand for?
A. Central Processing Unit
B. Computer Program Utility
C. Central Power Unit
D. Computer Performance Unit
Answer: A
Explanation: The CPU, or Central Processing Unit, is the primary component of a computer that performs most of the processing inside a computer.

The difficulty level should be {difficulty_prompt}
"""
    print(f"[Prompt Sent to Gemini]:\n{prompt}")

    try:
        response = model.generate_content(prompt)
        if not hasattr(response, 'text') or not response.text:
            raise ValueError("Gemini response did not return text.")
        content = response.text.strip()

        lines = content.split("\n")
        question = ""
        choices = []
        answer_letter = ""
        explanation = ""
        question_found = False

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith(("A.", "B.", "C.", "D.")):
                choices.append(line[3:].strip())
            elif line.startswith("Answer:"):
                answer_letter = line.replace("Answer:", "").strip().upper()
            elif line.startswith("Explanation:"):
                explanation = line.replace("Explanation:", "").strip()
            elif not question_found:
                question = line
                question_found = True

        answer_index = ord(answer_letter) - ord('A')
        answer_text = choices[answer_index] if 0 <= answer_index < len(choices) else "Unknown"

        return {
            'question': question,
            'choices': choices,
            'answer': answer_text,
            'answer_letter': answer_letter,
            'explanation': explanation,
            'difficulty': difficulty,
            'question_text': question
        }

    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return {
            'question': "Error generating question.",
            'choices': ["A", "B", "C", "D"],
            'answer': "A",
            'explanation': str(e),
            'difficulty': difficulty,
            'question_text': "Error generating question."
        }


def generate_hint(question_text):
    if MOCK_MODE:
        return "It's an organelle that produces ATP, often referred to as the energy factory."

    try:
        prompt = f"Provide a helpful hint for this quiz question without revealing the answer: {question_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error fetching hint: {str(e)}"


def follow_up_response(followup_prompt, attempt_count=0):
    if MOCK_MODE:
        if attempt_count < 3:
            return (
                "That's a thoughtful try! Let's break it down together:\n\n"
                "• Nucleus: Acts as the cell’s control center, storing genetic material (DNA) and directing activities—it doesn’t make energy.\n"
                "• Ribosome: These small structures are responsible for assembling proteins but not producing cellular energy.\n"
                "• Chloroplast: Found in plant cells, chloroplasts convert sunlight into food through photosynthesis. While important, they don’t generate ATP directly.\n\n"
                "Think about what produces ATP—the cell’s fuel—and how each organelle contributes differently to cellular life."
            )
        else:
            return (
                "You're really giving this your all—great persistence!\n\n"
                "The nucleus handles genetic control, ribosomes build proteins, and chloroplasts handle photosynthesis in plants. But only one organelle is directly responsible for producing ATP—the main energy carrier in the cell. Think about which one that is!"
            )

    lower_prompt = followup_prompt.lower()
    banned_phrases = [
        "what's the answer", "what is the answer", "give me the answer",
        "which one is correct", "is it", "correct answer",
        "choose the right one", "is the answer", "tell me the answer"
    ]
    if any(phrase in lower_prompt for phrase in banned_phrases):
        if attempt_count < 3:
            return (
                "Not just yet! Let's go over the options to help you out:\n\n"
                "• Nucleus: Directs cell activity and holds DNA, but doesn't create energy.\n"
                "• Ribosome: Builds proteins—important, but not related to energy.\n"
                "• Chloroplast: Converts sunlight into food in plants—photosynthesis, not energy for cellular work.\n\n"
                "Think carefully—which one is actually known for making ATP, the cell’s fuel?"
            )
        else:
            return ("You've made several attempts—keep going!\n\n"
                    "Nucleus: Stores genetic material and regulates the cell, but does not produce energy.\n"
                    "Ribosome: Synthesizes proteins, not involved in energy production.\n"
                    "Chloroplast: Converts sunlight into sugar in plants, not ATP.\n\n"
                    "Focus on which organelle produces ATP, the cell’s main energy source.")

    try:
        formatted = (
            f"A student asked: '{followup_prompt}'.\n"
            f"Please provide a helpful explanation or clarification, without revealing the quiz answer directly. Keep the tone friendly and educational."
        )
        response = model.generate_content(formatted)
        return response.text.strip()
    except Exception as e:
        return f"Error fetching follow-up: {str(e)}"


# some handy functions moved over from gui.py to keep things tidy
def evaluate_answer(user_answer, correct_answer_letter):
    is_correct = user_answer.strip().upper() == correct_answer_letter.strip().upper()
    return is_correct

def generate_final_score_message(score, total):
    percentage = (score / total) * 100
    if percentage == 100:
        return "Perfect score! You're a quiz master!"
    elif percentage >= 80:
        return "Great job! You’ve mastered most of the material."
    elif percentage >= 60:
        return "Not bad! Review a few areas to strengthen your understanding."
    else:
        return "Keep studying! Let’s go over the topics again for better retention."

def deduplicate_question(topic, seen_questions, difficulty="easy"):
    retries = 5
    last_question = None
    while retries > 0:
        question_data = generate_quiz_question(topic, difficulty, seen_questions)
        if question_data and question_data['question_text'] not in seen_questions:
            return question_data
        last_question = question_data
        retries -= 1
    return last_question or {
        'question': "Failed to generate a unique question.",
        'choices': ["A", "B", "C", "D"],
        'answer': "A",
        'answer_letter': "A",
        'explanation': "No explanation available.",
        'difficulty': difficulty,
        'question_text': "Failed to generate a unique question."
    }

def generate_feedback(user_answer, correct_letter, explanation, difficulty="easy"):
    if user_answer.strip().upper() == correct_letter.strip().upper():
        return "Correct! Here's why: " + explanation
    else:
        return "Not quite. Here's why that's not correct: " + explanation + " Please try again!"


# this class keeps track of the quiz progress, score, hints, and all that jazz
class QuizSession:
    def __init__(self, topic, difficulty="easy"):
        self.topic = topic
        self.difficulty = difficulty
        self.score = 0
        self.total_questions = 0
        self.seen_questions = set()
        self.max_questions = 5
        self.current_question_number = 1
        self.wrong_attempts = 0
        self.correct_count = 0

    def next_question(self):
        question_data = deduplicate_question(self.topic, self.seen_questions, self.difficulty)
        if not question_data:
            return None  # no more fresh questions from Gemini

        self.current_question_text = question_data['question_text']
        self.correct_letter = question_data['answer_letter']
        self.explanation = question_data['explanation']
        self.current_question_number += 1
        self.total_questions += 1
        return question_data

    def submit_answer(self, user_answer, correct_letter):
        is_correct = evaluate_answer(user_answer, correct_letter)
        self.seen_questions.add(self.current_question_text)
        # note: we only bump total_questions when we load a new question, not here
        if is_correct:
            self.score += 1
            self.correct_count += 1
        else:
            self.wrong_attempts += 1
        feedback = generate_feedback(user_answer, correct_letter, self.explanation, self.difficulty)
        return is_correct, feedback

    def get_score_message(self):
        return generate_final_score_message(self.score, self.total_questions)

    def is_finished(self):
        return self.current_question_number > self.max_questions

    def get_hint(self):
        return generate_hint(self.explanation)

    def score_percentage(self):
        if self.total_questions == 0:
            return 0
        return (self.correct_count / self.total_questions) * 100  # just a simple percentage calculation