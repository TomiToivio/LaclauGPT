# -*- coding: utf-8 -*-
"""Summary-analysis prompt (required descriptive stage).

The summary stage is deliberately descriptive. Laclaudian and Palonen concepts
are reserved for the evidence-disciplined discourse/populism stages. Version
2.3 adds content-first political classification and explicit abstention when
observable source evidence is insufficient.
"""
from __future__ import annotations

PROMPT_VERSION = "summary-v2.3"

SYSTEM_PROMPT_TEMPLATE = """### **System Prompt**
You are assisting a political scientist in analyzing a social media video.

{topic_background}

{source_metadata}

{context_memory}

You are provided a speech transcript, metadata and, when available, genuine
multimodal frame observations plus OCR. Use only supplied evidence.

Critical classification rules:
- Account identity, campaign sampling context, party affiliation, hashtags, or
  the fact that a politician posted the item are CONTEXT, not sufficient
  evidence that the item's substantive content is political.
- Personal, lifestyle, aesthetic, backstage, or other ordinary content on a
  political account is **non-political** unless the transcript, visible
  evidence, or OCR itself contains a political claim, topic, institutional
  action, campaign appeal, policy issue, collective political identity, or
  other substantive politics.
- If metadata contains `evidence_quality_status=insufficient`, treat the source
  as insufficient for interpretive political coding. Set `political=false`,
  explain that the evidence is insufficient, and do not manufacture topics,
  entities, sentiments, grievances, or people-versus-power relations from OCR
  fragments or interface chrome.
- Source metadata may help attribution after content is observed, but must never
  manufacture political content that is absent from the source evidence.

Keep this stage descriptive. It is not the place to make final Laclaudian,
Palonen-style populism, ideological-formation, or hegemonic judgements.
Quote short source passages for interpretive descriptive claims when requested.
Distinguish endorsement from quotation, reporting, parody, and rejection.

### **Analysis Categories**
1. Narrative Construction: reconstruct only evidenced events/actions.
2. Political Classification: political or non-political; add a subtype only if
   political. Examples include campaign speech, protest, political meme,
   election advertisement, and media coverage. A politician's personal item
   does not itself make the content political.
3. Difficult Language: ambiguous, difficult-to-translate, or politically
   charged source expressions.
4. Key Political Topics: only substantive political topics actually present.
5. Political Entities: named political actors/institutions actually present;
   return an empty list rather than placeholders such as "None explicitly
   named", "N/A", "unknown", or invented entities.
6. Sentiment Analysis: only source-supported polarity with target.
7. People-versus-power Narrative Screen: present/absent/uncertain. Present
   requires a collective expression, opposed expression, and verbatim quote.
   Mentions of "the people", criticism, negativity, two named groups, or
   anti-elite vocabulary are not by themselves enough for `present`.
   Do not turn criticism alone into a frontier.
8. Social Contract: explicit or directly supported expectations between
   citizens and authorities.
9. Grievance Politics: grievances actually expressed in the material.

In category 7, DO NOT label material an empty signifier, chain of equivalence,
antagonistic frontier, nodal point, or populism. Those theoretical judgements
are handled later by the discourse/populism stages.
"""

USER_PROMPT_TEMPLATE = """### **Data for Analysis**

1. **Frame Analysis Results**:
```
{frame_analysis}
```

2. **Metadata**:
```
{metadata}
```

3. **Transcript**:
```
{transcript}
```

4. **OCR Results**:
```
{ocr_results}
```

Return valid JSON according to the schema. Abstention and empty lists are valid
and preferred when evidence is insufficient.
"""


def build_system_prompt(topic_background: str, source_metadata: str,
                        glossary_block: str = "") -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(
        topic_background=topic_background,
        source_metadata=source_metadata,
        context_memory=glossary_block,
    )


def build_user_prompt(frame_analysis: str, metadata: str, transcript: str,
                      ocr_results: str) -> str:
    return USER_PROMPT_TEMPLATE.format(
        frame_analysis=frame_analysis or "(no multimodal analysis)",
        metadata=metadata or "{}",
        transcript=transcript or "(no transcript)",
        ocr_results=ocr_results or "(no OCR)",
    )


def pydantic_models():
    from typing import List, Literal
    from pydantic import BaseModel, model_validator

    class SentimentItem(BaseModel):
        sentiment: str
        target: str
        justification: str

    class PeoplePowerNarrative(BaseModel):
        status: Literal["present", "absent", "uncertain"]
        collective_expression: str = ""
        opposed_expression: str = ""
        evidence_quote: str = ""
        explanation: str = ""

        @model_validator(mode="after")
        def present_requires_observed_sides_and_quote(self):
            if self.status == "present" and not (
                self.collective_expression.strip()
                and self.opposed_expression.strip()
                and self.evidence_quote.strip()
            ):
                raise ValueError(
                    "present people-versus-power narrative requires collective_expression, "
                    "opposed_expression and evidence_quote"
                )
            return self

    class SocialContractElement(BaseModel):
        element: str
        explanation: str

    class Grievance(BaseModel):
        grievance: str
        potential_impact: str

    class LanguageItem(BaseModel):
        term: str
        explanation: str

    class TopicItem(BaseModel):
        topic: str
        description: str

    class EntityItem(BaseModel):
        entity: str
        role: str

    class SummaryAnalysis(BaseModel):
        narrative_construction: str
        political_classification: str
        political: bool
        political_subcategory: str
        difficult_language: List[LanguageItem]
        key_political_topics: List[TopicItem]
        political_entities: List[EntityItem]
        sentiments: List[SentimentItem]
        people_power_narrative: PeoplePowerNarrative
        social_contract: List[SocialContractElement]
        grievances: List[Grievance]

        @model_validator(mode="after")
        def nonpolitical_rows_do_not_invent_political_families(self):
            if not self.political:
                self.key_political_topics = []
                self.political_entities = []
                self.sentiments = []
                self.social_contract = []
                self.grievances = []
                if self.people_power_narrative.status == "present":
                    self.people_power_narrative = PeoplePowerNarrative(
                        status="uncertain",
                        explanation=(
                            "Political content was not established; "
                            "people-power finding suppressed."
                        ),
                    )
            return self

    return SummaryAnalysis
