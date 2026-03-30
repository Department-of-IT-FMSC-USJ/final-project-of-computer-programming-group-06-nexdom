"""
RAG CHATBOT - Using Google Gemini API
1. RETRIEVES data from database
2. AUGMENTS prompt with data as context
3. GENERATES response using Gemini LLM
"""

from google import genai
from google.genai import types
from chatbot.data_analyzer import DataRetriever


class RAGChatBot:
    def __init__(self, api_key, db_manager, name="HomeHelper"):
        self.__name = name
        self.__retriever = DataRetriever(db_manager)
        self.__model = "gemini-2.5-flash"

        # Connect to Gemini
        try:
            self.__client = genai.Client(api_key=api_key)
            self.__is_connected = True
        except Exception:
            self.__is_connected = False

        # System prompt
        self.__system_prompt = """
You are HomeHelper, an AI assistant for a Home Service Provider Platform.
Help customers find the best service providers based on reviews and ratings.

RULES:
1. ONLY use the provided data. Do NOT make up information.
2. When recommending, explain WHY based on actual reviews.
3. Mention rating, experience, price, and location.
4. Be friendly and concise.
5. Use emojis and bold formatting.
6. Give a final recommendation at the end.
"""

    def is_connected(self):
        return self.__is_connected

    def chat(self, user_message):
        """Main RAG chat method"""
        if not self.__is_connected:
            return "❌ Not connected. Please check your API key."

        try:
            # STEP 1: RETRIEVE - get data from database
            context_data = self.__retriever.build_context_for_query(user_message)

            # STEP 2: AUGMENT - combine system prompt + data + question
            full_prompt = f"""
{self.__system_prompt}

===== DATA FROM OUR DATABASE =====
{context_data}
===== END OF DATA =====

CUSTOMER'S QUESTION: {user_message}

Answer based ONLY on the data above.
"""

            # STEP 3: GENERATE - send to Gemini LLM
            response = self.__client.models.generate_content(
                model=self.__model,
                contents=[types.Part.from_text(text=full_prompt)]
            )
            return response.text

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def get_service_recommendation(self, service_type):
        """Quick recommendation for a service"""
        return self.chat(
            f"Find me the best {service_type} provider. "
            f"Compare all and recommend the best one with reasons."
        )

    def compare_providers(self, service_type):
        """Compare providers for a service"""
        return self.chat(
            f"Compare all {service_type} providers. "
            f"Rank them by rating, reviews, experience, and price."
        )