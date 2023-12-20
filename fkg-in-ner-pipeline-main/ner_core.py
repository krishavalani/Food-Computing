import spacy
import re

from spacy.tokens.span import Span
from typing import Dict, AnyStr

class NER:
	"""
		A wrapper over the spacy.Language instance, which will be used to perform NER (and any other tasks we may want to do in the future).
		Caches entities and their labels.
	"""

	def __init__(self, nlp: spacy.Language, use_ruler: bool = True):
		self.lang: spacy.Lang = nlp
		self.spanned_entities_by_text: Dict[str, list[Span]] = {}
		self.entities: Dict[str, str] = {}
		self.ruler: spacy.pipeline.EntityRuler = None	
		self.regexes: Dict[str, list[re.Pattern[AnyStr]]] = {}
		if use_ruler:
			self.ruler = self.lang.add_pipe("entity_ruler", config = {"validate": True, "overwrite_ents": True})

	def add_label_pattern(self, label: str, pattern: list[Dict]) -> None:
		self.add_label_patterns(label, [pattern])

	def add_label_patterns(self, label: str, patterns: list[list[Dict]]) -> None:
		if self.ruler == None:
			raise ValueError("NER instance not using the entity ruler.")
		self.ruler.add_patterns([{"label": label, "pattern": pattern} for pattern in patterns])
		
	def add_sentence_regex(self, label: str, regex: str) -> None:
		self.add_sentence_regexes(label, [regex])

	def add_sentence_regexes(self, label: str, regexes: list[str]) -> None:
		regexes = [re.compile(regex, ) for regex in regexes]
		self.regexes.setdefault(label, []).extend(regexes)

	# TODO: r/w sentence regexes to/from disk
	def patterns_to_disk(self, outfile: str) -> None:
		self.ruler.to_disk(outfile)

	def patterns_from_disk(self, infile: str) -> None:
		self.ruler.from_disk(infile)

	def get_doc(self, text: str) -> spacy.tokens.Doc:
		return self.lang(text) 

	def eval(self, text: str) -> dict:
		doc = self.get_doc(text)
		regex_spans = []
		ner = {}

		for label, regexes in self.regexes.items():
			for regex in regexes:
				for match in regex.finditer(text):
					matched_text = match.group()
					start, end = match.span()
					labelled_span = doc.char_span(start, end, label = label)
					
					ner.update({matched_text: label})
					self.entities.update({matched_text: label})
					regex_spans.append(labelled_span)

		for ent in doc.ents:
			ner[ent.text] = ent.label_
			self.entities.update({ent.text: ent.label_})

		self.spanned_entities_by_text[text] = regex_spans + list(doc.ents)

		return ner