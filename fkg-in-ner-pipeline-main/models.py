import spacy

SPACY_EN_MODELS = {"SMALL": "en_core_web_sm", "MEDIUM": "en_core_web_md", "LARGE": "en_core_web_lg", "TRANSFORMER": "en_core_web_trf"}

def spacy_base_en(model: str = "SMALL") -> spacy.Language:
	"""
		Returns a spacy.Language instance with the specified model.
	"""

	model = model.upper()

	if model not in SPACY_EN_MODELS:
		raise ValueError(f"Invalid model name: {model}")

	return spacy.load(SPACY_EN_MODELS[model])