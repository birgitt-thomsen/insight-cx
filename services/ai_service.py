"""This script handles the AI call for feedback analysis."""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from services.prompt_service import PromptService
from schemas.feedback_analysis_schema import FEEDBACK_ANALYSIS_SCHEMA

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class AIService:

    def __init__(self):
        self.prompt_service = PromptService()

    def _supports_temperature(
            self,
            model,
    ):
        """
        Return True if the selected model
        supports the temperature parameter.
        """

        return not model.startswith(
            "gpt-5"
        )

    def analyze_feedback(
            self,
            feedback_text: str
    ) -> dict:
        """
        Analyze feedback using the current production
        model and prompts.
        """

        config = (
            self.prompt_service
            .get_feedback_prompts()
        )

        analysis = self.execute_prompt(
            feedback_text,
            config
        )

        return {
            "analysis": analysis,

            "model": config["model"],

            "temperature": config["temperature"],

            "system_prompt_version":
                config["system_prompt_version"],

            "feedback_prompt_version":
                config["feedback_prompt_version"],
        }

    def execute_prompt(
            self,
            feedback_text: str,
            config: dict,
    ):
        """
        Execute a feedback analysis prompt.
        """

        user_prompt = (
            config["feedback_prompt"]
            .replace(
                "{{feedback}}",
                feedback_text
            )
        )

        request = {

            "model": config["model"],

            "input": [

                {
                    "role": "system",
                    "content": config["system_prompt"],
                },

                {
                    "role": "user",
                    "content": user_prompt,
                },

            ],

            "text": {

                "format": {

                    "type": "json_schema",

                    "name": "feedback_analysis",

                    "strict": True,

                    "schema": FEEDBACK_ANALYSIS_SCHEMA,

                }

            }

        }

        if self._supports_temperature(
                config["model"]
        ):
            request["temperature"] = (
                config["temperature"]
            )

        response = client.responses.create(
            **request
        )

        return json.loads(
            response.output_text
        )


    def execute_test_prompt(
            self,
            feedback_text: str,
            model=None,
            temperature=None,
            system_prompt_version=None,
            feedback_prompt_version=None,
    ):
        """
        Execute a prompt test with optional overrides.

        Does not save anything.
        """

        config = (
            self.prompt_service
            .get_feedback_prompts(
                model=model,
                temperature=temperature,
                system_prompt_version=system_prompt_version,
                feedback_prompt_version=feedback_prompt_version,
            )
        )

        return self.execute_prompt(
            feedback_text,
            config
        )

    # def _parse_and_validate_json(self, content: str) -> dict:
    #     """
    #     Try to parse the model output as JSON and do a minimal sanity check.
    #     Raises ValueError if something is clearly wrong.
    #     """
    #     try:
    #         response = json.loads(content)
    #     except json.JSONDecodeError as e:
    #         raise ValueError(
    #             f"Model returned invalid JSON: {e}\nRaw content: {content!r}")
    #
    #     # Basic structure check
    #     required_keys = ["sentiment", "emotion", "confidence", "priority",
    #                      "themes", "summary"]
    #     for key in required_keys:
    #         if key not in response:
    #             raise ValueError(
    #                 f"Missing key in JSON output: {key}. Got: {response}")
    #
    #     if not isinstance(response["sentiment"], str):
    #         raise ValueError(
    #             f"sentiment must be a string, got:"
    #             f" {type(response['sentiment'])}")
    #     if not isinstance(response["emotion"], str):
    #         raise ValueError(
    #             f"emotion must be a string, got: {type(response['emotion'])}")
    #     if not isinstance(response["confidence"], (int, float)):
    #         raise ValueError(
    #             f"confidence must be a number, got: {type(response['confidence'])}")
    #     if not isinstance(response["priority"], str):
    #         raise ValueError(
    #             f"priority must be a string, got:"
    #             f" {type(response['priority'])}")
    #     if not isinstance(response["themes"], list):
    #         raise ValueError(
    #             f"themes must be a list, got: {type(response['themes'])}")
    #     if not isinstance(response["summary"], str):
    #         raise ValueError(
    #             f"summary must be a string, got: {type(response['summary'])}")
    #
    #     return response
