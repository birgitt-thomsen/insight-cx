"""
Central configuration for the OpenAI models used by the application.

Every place that needs the list of models, the default model,
temperature support or pricing should import it from here.
"""

DEFAULT_MODEL = "gpt-6-luna"

# Models offered in the UI and used for benchmark comparisons.
AVAILABLE_MODELS = [
    "gpt-6-luna",
    "gpt-6.1-sol",
    "gpt-6-astra",
]

MODEL_LABELS = {
    "gpt-6-luna": "GPT-6 Luna",
    "gpt-6.1-sol": "GPT-6.1 Sol",
    "gpt-6-astra": "GPT-6 Astra",
}

# Models that accept the temperature parameter.
# Temperature is omitted for every other model, which avoids
# request errors on reasoning models that reject it.
TEMPERATURE_SUPPORTED_MODELS = set()

# Prices are USD per 1 million tokens.
# Models without pricing are benchmarked with an estimated cost of 0.
MODEL_PRICING = {
    # "gpt-6-luna": {"input": 0.10, "output": 0.50},
    # "gpt-6.1-sol": {"input": 2.00, "output": 10.00},
    # "gpt-6-astra": {"input": 10.00, "output": 50.00},
}


def supports_temperature(model):
    """
    Return True if the model supports the temperature parameter.
    """

    return model in TEMPERATURE_SUPPORTED_MODELS


def normalize_model(model):
    """
    Return the model if it is supported, otherwise the default model.

    Used to migrate settings that still reference retired models.
    """

    if model in AVAILABLE_MODELS:
        return model

    return DEFAULT_MODEL
