# -*- coding: utf-8 -*-
"""Postprocess prompt (structured descriptive extraction).

The postprocess stage is shared by topics, entities and descriptive sentiment,
but the canonical project switches are authoritative: disabled families are not
requested from the model. Version 2.4 adds placeholder filtering and explicit
abstention for non-political or evidence-insufficient material.
"""
from __future__ import annotations

PROMPT_VERSION = "postprocess-v2.4"
_PLACEHOLDERS = {
    "none", "none explicitly named", "none named", "n/a", "na", "unknown",
    "not applicable", "no entity", "no entities", "unspecified", "nil",
}


def _valid_label(value: str) -> bool:
    text = " ".join(str(value or "").strip().casefold().split())
    return bool(text) and text not in _PLACEHOLDERS


def build_system_prompt(
    glossary_block: str = "",
    *,
    include_topics: bool = True,
    include_entities: bool = True,
    include_sentiment: bool = True,
) -> str:
    tasks: list[str] = []
    output_fields: list[str] = []

    if include_topics:
        tasks.append("""1. **Extract Topics**:
- Extract topics actually present in the source/analysis.
- Match established topics first; propose only genuinely new topics.
- If the preliminary summary is non-political or says evidence is insufficient,
  do not manufacture political topics from account identity or metadata.
- If no substantive topic is supported, return an empty list.""")
        output_fields.extend(["topics", "new_topics"])

    if include_entities:
        tasks.append("""2. **Extract Entities**:
- Extract named entities actually mentioned in the source/analysis.
- Entity presence never implies endorsement, authorship, ideology or sentiment.
- Match the established entity list first and use its canonical form when a
  supported match exists; keep weak or ambiguous matches out rather than
  guessing.
- NEVER emit placeholders such as `None`, `None explicitly named`, `N/A`,
  `unknown`, `unspecified` or similar as entities.
- If no entity is present, return an empty list.
- Classify each matched entity with exactly one spaCy NER type from this closed
  list: PERSON, NORP, FAC, ORG, GPE, LOC, PRODUCT, EVENT, WORK_OF_ART, LAW,
  LANGUAGE, DATE, TIME, PERCENT, MONEY, QUANTITY, ORDINAL, CARDINAL.""")
        output_fields.extend(["entities", "entity_types", "new_entities"])

    if include_sentiment:
        tasks.append("""3. **Determine descriptive sentiment**:
- Identify only source-supported positive, neutral or negative sentiment in the
  document author's or speaker's OWN ASSERTED VOICE and its target.
- Return target, polarity, one short verbatim evidence quote, and uncertainty.
- Do not infer sentiment from ideology, account identity, or disagreement.
- If the summary is non-political or evidence is insufficient, ordinary
  personal content need not receive political sentiment coding.
- If attribution or polarity is unclear, abstain rather than guessing.
- `sentiments` is descriptive polarity only, not Laclaudian affective
  investment.""")
        output_fields.extend(["sentiments", "positive", "neutral", "negative"])

    if not tasks:
        tasks.append("No descriptive coding family is enabled. Return the empty schema.")

    disabled = []
    if not include_topics:
        disabled.extend(["topics", "new_topics"])
    if not include_entities:
        disabled.extend(["entities", "entity_types", "new_entities"])
    if not include_sentiment:
        disabled.extend(["sentiments", "positive", "neutral", "negative"])

    return f"""### System Prompt

**Role**:
You are presented source material plus a preliminary analysis. Extract only the
descriptive coding families enabled below. This stage is descriptive and does
not make final discourse-theoretical claims. Empty lists are valid and preferred
to placeholder or inferred content.

Retrieved codebook candidates (not evidence):
{glossary_block}

---

**Enabled tasks**:

{chr(10).join(tasks)}

---

**Output format**:
Return one strict JSON object. Enabled fields are: {', '.join(output_fields) or '(none)'}.
The full schema also contains disabled fields; they MUST be empty when disabled:
{', '.join(disabled) or '(none)'}.
"""


def pydantic_models():
    from typing import Literal

    from laclaugpt_memory import NER_TYPES
    from pydantic import BaseModel, Field, field_validator, model_validator

    class SentimentReading(BaseModel):
        target: str = Field(min_length=1)
        polarity: Literal["positive", "neutral", "negative"]
        evidence_quote: str = Field(min_length=1)
        uncertainty: float = Field(default=0.0, ge=0.0, le=1.0)

    class Extraction(BaseModel):
        topics: list[str] = []
        entities: list[str] = []
        entity_types: list[str] = []
        positive: list[str] = []
        neutral: list[str] = []
        negative: list[str] = []
        new_topics: list[str] = []
        new_entities: list[str] = []
        sentiments: list[SentimentReading] = []

        @field_validator("entity_types")
        @classmethod
        def _ner_types_closed_vocabulary(cls, values):
            return [value if value in NER_TYPES else "" for value in values]

        @model_validator(mode="after")
        def _drop_placeholders_without_breaking_entity_type_alignment(self):
            old_entities = list(self.entities)
            old_types = list(self.entity_types)
            kept_entities: list[str] = []
            kept_types: list[str] = []
            for index, entity in enumerate(old_entities):
                if not _valid_label(entity):
                    continue
                kept_entities.append(entity)
                kept_types.append(old_types[index] if index < len(old_types) else "")
            self.entities = kept_entities
            self.entity_types = kept_types
            self.new_entities = [v for v in self.new_entities if _valid_label(v)]
            self.topics = [v for v in self.topics if _valid_label(v)]
            self.new_topics = [v for v in self.new_topics if _valid_label(v)]
            self.positive = [v for v in self.positive if _valid_label(v)]
            self.neutral = [v for v in self.neutral if _valid_label(v)]
            self.negative = [v for v in self.negative if _valid_label(v)]
            self.sentiments = [s for s in self.sentiments if _valid_label(s.target)]
            return self

    return Extraction
