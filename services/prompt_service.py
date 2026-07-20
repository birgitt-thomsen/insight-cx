from pathlib import Path
from storage.ai_settings_storage import AISettingsStorage

class PromptService:
    """Loads prompt files from disk."""

    def __init__(self):
        """Locate prompts directory."""

        self.prompts_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
        )

        self.ai_settings_storage = (
            AISettingsStorage()
        )

    def load(self, prompt_type, version):
        """
        Load a prompt file.

        Args:
            prompt_type (str): e.g. "system" or "feedback"
            version (str): e.g. "v1"

        Returns:
            str: Prompt text.
        """

        prompt_file = (
            self.prompts_path
            / prompt_type
            / f"{version}.txt"
        )

        if not prompt_file.exists():
            raise FileNotFoundError(
                f"Prompt not found: {prompt_file}"
            )

        return prompt_file.read_text(
            encoding="utf-8"
        )

    def get_prompts(
            self,
            model=None,
            system_prompt_version=None,
            feedback_prompt_version=None,
    ):
        """
		Return the prompts and model to use.

		If values are supplied they are used.
		Otherwise, the active AI settings are loaded.
		"""

        if (
                model is None
                or system_prompt_version is None
                or feedback_prompt_version is None
        ):
            settings = (
                self.ai_settings_storage.get_settings()
            )

            model = settings.model

            system_prompt_version = (
                settings.system_prompt_version
            )

            feedback_prompt_version = (
                settings.feedback_prompt_version
            )

        return {

            "model": model,

            "system_prompt": self.load(
                "system",
                system_prompt_version
            ),

            "feedback_prompt": self.load(
                "feedback",
                feedback_prompt_version
            ),

            "system_prompt_version":
                system_prompt_version,

            "feedback_prompt_version":
                feedback_prompt_version,

        }

    def get_versions(self, prompt_type):
        """
        Return all available versions for a prompt type.

        Example:
            ["v1", "v2", "v3"]
        """

        prompt_dir = (
                self.prompts_path
                / prompt_type
        )

        return sorted(
            file.stem
            for file in prompt_dir.glob("*.txt")
        )
