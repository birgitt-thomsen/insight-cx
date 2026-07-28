"""This script handles database operations for AI settings."""

from models import db, AISettings


class AISettingsStorage:
    """Handles the application's AI configuration."""

    def get_settings(self):
        """
        Return the application's AI settings.

        If no settings exist yet, create the default row.
        """

        settings = db.session.get(
            AISettings,
            1
        )

        if settings is None:

            settings = AISettings()

            db.session.add(settings)
            db.session.commit()

        return settings

    def update_feedback_settings(
            self,
            feedback_model,
            feedback_temperature,
            system_prompt_version,
            feedback_prompt_version,
            description,
    ):
        """
        Update feedback analysis AI configuration.
        """

        settings = self.get_settings()

        settings.feedback_model = (
            feedback_model
        )

        settings.feedback_temperature = (
            feedback_temperature
        )

        settings.system_prompt_version = (
            system_prompt_version
        )

        settings.feedback_prompt_version = (
            feedback_prompt_version
        )

        settings.description = description

        db.session.commit()

        return settings

    def update_executive_settings(
            self,
            executive_model,
            executive_temperature,
            executive_prompt_version,
            description=None,
    ):
        """
        Update executive summary AI configuration.
        """

        settings = self.get_settings()

        settings.executive_model = (
            executive_model
        )

        settings.executive_temperature = (
            executive_temperature
        )

        settings.executive_prompt_version = (
            executive_prompt_version
        )

        if description:
            settings.description = description

        db.session.commit()

        return settings
