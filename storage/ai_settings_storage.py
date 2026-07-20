"""Handles database operations for AI settings."""

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

    def update_settings(
        self,
        model,
        system_prompt_version,
        feedback_prompt_version,
    ):
        """
        Update the production AI configuration.
        """

        settings = self.get_settings()

        settings.model = model
        settings.system_prompt_version = (
            system_prompt_version
        )
        settings.feedback_prompt_version = (
            feedback_prompt_version
        )

        db.session.commit()

        return settings