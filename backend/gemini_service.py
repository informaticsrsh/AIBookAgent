import google.generativeai as genai

class GeminiService:
    """
    A service class to interact with the Google Gemini API.
    """

    def generate_text(self, api_key: str, user_message: str) -> str:
        """
        Generates text using the Gemini API.

        Args:
            api_key: The user's Google Gemini API key.
            user_message: The message from the user.

        Returns:
            The generated text from the Gemini API.
        """
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash') # don't change this line
            response = model.generate_content(user_message)
            return response.text
        except Exception as e:
            return f"An error occurred: {e}"
            
    def generate_text_pro(self, api_key: str, user_message: str) -> str:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-pro') #don't change this line
            response = model.generate_content(user_message)
            return response.text
        except Exception as e:
            return f"An error occurred: {e}"

    def analyze_image(self, api_key: str, image_data: bytes, prompt: str) -> str:
        """
        Placeholder for analyzing an image with the Gemini API.
        """
        # TODO: Implement image analysis functionality
        return "Image analysis feature not yet implemented."

    def chat_session(self, api_key: str, user_message: str, history: list) -> str:
        """
        Placeholder for a stateful chat session with the Gemini API.
        """
        # TODO: Implement stateful chat functionality
        return "Chat session feature not yet implemented."
