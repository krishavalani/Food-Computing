from typing import Dict
import re

def re2pat(regex: str) -> Dict:
	"""
	Converts a given regular expression to a spaCy single-token pattern.
	"""
	try:
		re.compile(regex)
	except:
		raise ValueError(f"Invalid regular expression: {regex}")

	# return the incoming regex, since python's regex /= spacy's regex
	return {"TEXT": {"REGEX": regex}}

if __name__ == "__main__":
	print(re2pat("/(a|b){2,4}c/i"))