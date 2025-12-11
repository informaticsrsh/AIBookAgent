import google.generativeai as genai
import time
from collections import deque

class GeminiService:
    """
    A service class to interact with the Google Gemini API.
    """

    def __init__(self):
        self.flash_request_timestamps = deque()
        self.pro_request_timestamps = deque()
        self.flash_rpm = 15
        self.pro_rpm = 2

    def rate_limit_wait(self, timestamps: deque, rpm: int):
        """
        Waits if the number of requests in the last minute exceeds the RPM limit.
        """
        if not rpm:
            return

        while len(timestamps) >= rpm:
            time_since_oldest_request = time.time() - timestamps[0]
            if time_since_oldest_request < 60:
                time.sleep(60 - time_since_oldest_request)
            else:
                timestamps.popleft()

        timestamps.append(time.time())


    def generate_flash_response(self, api_key: str, user_message: str, system_instructions: str = None, response_mime_type: str = "text/plain") -> str:
        """
        Generates text using the Gemini Flash model.
        """
        self.rate_limit_wait(self.flash_request_timestamps, self.flash_rpm)
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instructions)
            response = model.generate_content(user_message, generation_config={"response_mime_type": response_mime_type})
            return response.text
        except Exception as e:
            return f"An error occurred: {e}"

    def generate_pro_response(self, api_key: str, user_message: str, system_instructions: str = None, response_mime_type: str = "text/plain") -> str:
        """
        Generates text using the Gemini Pro model.
        """
        self.rate_limit_wait(self.pro_request_timestamps, self.pro_rpm)
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=system_instructions)
            response = model.generate_content(user_message, generation_config={"response_mime_type": response_mime_type})
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
