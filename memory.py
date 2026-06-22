from collections import deque


class ConversationMemory:
    """
    Stores recent conversations for context.

    Each memory item contains:
    - User question
    - Detected intent
    - Analysis result
    - AI response
    - Optional extracted parameters
    """

    def __init__(self, max_history=10):
        self.history = deque(maxlen=max_history)

    def add(
        self,
        question,
        intent,
        data,
        answer,
        parameters=None
    ):
        """
        Save one conversation.
        """

        if parameters is None:
            parameters = {}

        self.history.append(
            {
                "question": question,
                "intent": intent,
                "data": data,
                "answer": answer[:500],
                "parameters": parameters
            }
        )

    def get_context(self):
        """
        Return all stored conversations.
        """
        return list(self.history)

    def last(self):
        """
        Return the latest conversation.
        """
        if not self.history:
            return None

        return self.history[-1]

    def last_question(self):
        if not self.history:
            return None

        return self.history[-1]["question"]

    def last_intent(self):
        if not self.history:
            return None

        return self.history[-1]["intent"]

    def last_data(self):
        if not self.history:
            return None

        return self.history[-1]["data"]

    def last_answer(self):
        if not self.history:
            return None

        return self.history[-1]["answer"]

    def last_parameters(self):
        if not self.history:
            return {}

        return self.history[-1].get("parameters", {})

    def previous(self, index=1):
        """
        Return previous conversations.

        previous(1) -> last
        previous(2) -> second last
        """

        if len(self.history) < index:
            return None

        return self.history[-index]

    def clear(self):
        self.history.clear()

    def size(self):
        return len(self.history)


# Global memory object
memory = ConversationMemory()