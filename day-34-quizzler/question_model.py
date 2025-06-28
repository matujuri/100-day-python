import html

class Question:

    def __init__(self, q_text, q_answer):
        # unescape the html entities in the question text
        self.text = html.unescape(q_text)
        self.answer = q_answer
