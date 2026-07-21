import json
import os
from openai import OpenAI
from services.prompt_service import PromptService
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class AIService:

    def __init__(self):
        self.prompt_service = PromptService()

    def analyze_feedback(
        self,
        feedback_text: str
    ) -> dict:
        """
        Analyze feedback using the current production
        model and prompts.
        """

        response = self.test_prompt(
            feedback_text
        )

        # return json.loads(response) original version
        analysis = json.loads(response.output_text)

        return {
            "analysis": analysis,
            "model": self.model,
            "system_prompt_version": self.system_prompt_version,
            "feedback_prompt_version": self.feedback_prompt_version,
        }


    def test_prompt(
            self,
            feedback_text: str,
            model=None,
            system_prompt_version=None,
            feedback_prompt_version=None,
    ):
        """
        Execute the active production prompt.
        Returns parsed model output as a dictionary.
        """

        config = self.prompt_service.get_prompts(
            model=model,
            system_prompt_version=system_prompt_version,
            feedback_prompt_version=feedback_prompt_version,
        )

        user_prompt = (
            config["feedback_prompt"]
            .replace(
                "{{feedback}}",
                feedback_text
            )
        )

        response = client.responses.create(

            model=config["model"],

            input=[

                {
                    "role": "system",
                    "content": config["system_prompt"],
                },

                {
                    "role": "user",
                    "content": user_prompt,
                },

            ],

        )

        import json

        content = response.output_text.strip()

        try:
            return json.loads(content)

        except json.JSONDecodeError:
            raise ValueError(
                f"AI response was not valid JSON:\n{content}"
            )
