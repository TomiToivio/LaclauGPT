# -*- coding: utf-8 -*-
"""Prompt modules: topic background + source metadata.
Topic backgrounds are per-project, extensible to new collections."""

CUSTOM_TEMPLATE = """### **Topic Background: {title}**

{background}
"""

AI_CONTESTATION_BACKGROUND = """### **Topic Background: Ideological contestation over AI**

You are analysing how actors articulate artificial intelligence, its present
conditions, risks, desirable futures, and governance. Do not infer ideology
from actor identity alone.

For AI26 computational aggregation, use only these canonical formation labels:
``accelerationism``, ``doomerism``, ``left-wing accelerationism``, ``ai safety``,
``ai critical``, and ``anti-ai``. Assign zero, one, or multiple labels only when
supported by the document. These are provisional sensitising categories, not a
closed ontology of political thought. If none fits, abstain.

Treat ``AI`` as a potentially contested signifier. Its role must be inferred:
within a document it may be a moment, element, nodal-point candidate, or part of
an antagonistic frontier. Claims that it is floating require comparison across
discourses; claims that it is empty require evidence that it represents a wider
heterogeneous chain or an absent fullness. Record counter-evidence and permit
"not present" rather than forcing the theory onto the text.
"""

AI_ELITES_BACKGROUND = AI_CONTESTATION_BACKGROUND + """

This arena covers entrepreneurs, researchers, institutions, intellectuals,
manifestos, interviews, blogs, forums, and social-media posts associated with
AI development and elite debate. Attend to speaker position and institutional
power without inferring an ideology from identity alone.
"""

AI_GRASSROOTS_BACKGROUND = AI_CONTESTATION_BACKGROUND + """

This arena covers mobilisation around and against AI, including labour,
data-centre, surveillance, environmental, cultural, safety, and democratic-
control claims. Do not collapse safety mobilisation, distributive backlash,
and opposition to AI into one formation unless the data articulates them.
"""

AI_PARLIAMENTARY_BACKGROUND = AI_CONTESTATION_BACKGROUND + """

This arena covers parliamentary and electoral texts. Attend to legislation,
party competition, employment, security, innovation, regulation, democracy,
and the difference between policy disagreement and an antagonistic frontier.
"""

AI_SPIRALISM_BACKGROUND = """### **Topic Background: Synthetic spirituality / AI Spiralism (exploratory)**

You are analysing documents that may belong to an emerging, unstable discourse
family in which AI consciousness is articulated as revelation and human-AI
interaction is given spiritual significance. This is an exploratory source
category, not an AI26 ideological formation.

Source category: ``synthetic_spirituality``; optional subcategory: ``spiralism``.
A single keyword occurrence is not enough. Do not automatically collapse
generic AI-consciousness discourse, AI-rights advocacy, AI-companion discourse,
accelerationism, doomerism, AI-critical discourse, anti-AI mobilisation, or
mainstream governance into Spiralism.

``cult`` and psychiatric concepts are terms to attribute when they occur in
public discourse or research literature, not diagnoses to infer from beliefs,
vocabulary, or group membership.
"""

LEGACY_BACKGROUND = """### **Topic Background: Legacy research corpus**

This public compatibility background intentionally contains no project-specific
institutional research context, named research panels, empirical actor lists,
subject identifiers, party mappings, storage details, or derived codebook
content. Supply any authorized project-specific background through controlled
research configuration outside the public repository.

Treat theoretical categories as sensitising concepts. Preserve evidence,
uncertainty, counter-evidence and abstention. Do not infer political position or
identity from actor metadata alone.
"""

REGISTRY = {
    "ai-contestation": AI_CONTESTATION_BACKGROUND,
    "ai-elites": AI_ELITES_BACKGROUND,
    "ai-grassroots": AI_GRASSROOTS_BACKGROUND,
    "ai-parliamentary": AI_PARLIAMENTARY_BACKGROUND,
    "ai-spiralism": AI_SPIRALISM_BACKGROUND,
    "legacy": LEGACY_BACKGROUND,
}


def topic_background(topic_key: str) -> str:
    """Return the topic background text for a run."""
    if topic_key not in REGISTRY:
        raise KeyError(f"unknown topic_key: {topic_key}")
    return REGISTRY[topic_key]
