"""This script handles the ai call and creation of the executive summary."""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from services.prompt_service import PromptService
from storage.executive_insights_storage import ExecutiveInsightsStorage
from schemas.executive_summary_schema import EXECUTIVE_SUMMARY_SCHEMA


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

class ExecutiveSummaryService:

    def __init__(self):
        self.prompt_service = PromptService()
        self.executive_storage = ExecutiveInsightsStorage()

    def generate_summary(
            self,
            summary_data,
            model=None,
            temperature=None,
            system_prompt_version=None,
            executive_prompt_version=None,
    ) -> dict:
        """
        Generate and save an executive summary from
        an aggregated business dataset.
        """

        config = (
            self.prompt_service
            .get_executive_prompts(
                model=model,
                temperature=temperature,
                system_prompt_version=system_prompt_version,
                executive_prompt_version=executive_prompt_version,
            )
        )

        # FOR TESTING ONLY
        print("\nExecutive configuration")
        print("-----------------------")
        print(f"Requested model: {model}")
        print(f"Using model: {config['model']}")
        print(f"Prompt: {config['executive_prompt_version']}")

        summary = self.execute_prompt(
            summary_data,
            config
        )

        # FOR TESTING ONLY
        print("\n========== EXECUTIVE SUMMARY ==========\n")

        print(
            json.dumps(
                summary,
                indent=2
            )
        )

        # TURN OFF FOR TESTING ONLY
        self.executive_storage.save_summary(
            input_data=summary_data,
            summary=summary,
            config=config,
        )

        # FOR TESTING ONLY
        print("Saving executive summary...")
        print(f"Model: {config['model']}")
        print(f"Prompt: {config['executive_prompt_version']}")
        print(f"Generated: {datetime.utcnow()}")

        return {

            "summary": summary,

            "model": config["model"],

            "system_prompt_version":
                config["system_prompt_version"],

            "executive_prompt_version":
                config["executive_prompt_version"],

        }

    def execute_prompt(
            self,
            summary_data: dict,
            config: dict,
    ) -> dict:
        """
        Execute the executive summary prompt using
        Structured Outputs.
        """

        request = {

            "model": config["model"],

            "input": [

                {
                    "role": "system",
                    "content": config["system_prompt"],
                },

                {
                    "role": "user",
                    "content": json.dumps(
                        summary_data,
                        indent=2
                    ),
                },

            ],

            "text": {

                "format": {

                    "type": "json_schema",

                    "name": "executive_summary",

                    "strict": True,

                    "schema": EXECUTIVE_SUMMARY_SCHEMA,

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

        content = response.output_text.strip()

        try:

            summary = json.loads(content)

        except json.JSONDecodeError:

            raise ValueError(
                f"AI returned invalid JSON:\n\n{content}"
            )

        return summary

    def _supports_temperature(self, model):

        return not model.startswith(
            "gpt-5"
        )