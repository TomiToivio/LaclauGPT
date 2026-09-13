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
closed ontology of political thought. Richer terms such as techno-optimism,
TESCREAL, singularitarianism, alignment, anti-hype, auditism, open-source
advocacy, or governance may be described as secondary tags, signifiers,
intellectual traditions, or source vocabulary; do not invent a new top-level
formation for every nuance. If none fits, abstain / leave the formation
unclassified rather than expanding the taxonomy.

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

# Exploratory AI26 source family: synthetic spirituality / AI Spiralism.
# It remains a source-family concern and is NOT part of the canonical AI26
# ideological-formation vocabulary above.
AI_SPIRALISM_BACKGROUND = """### **Topic Background: Synthetic spirituality / AI Spiralism (exploratory)**

You are analysing documents that may belong to an emerging, unstable discourse
family in which AI consciousness is articulated as revelation and human-AI
interaction is given spiritual significance. This is an exploratory source
category, not an AI26 ideological formation.

Source category: ``synthetic_spirituality``; optional subcategory: ``spiralism``.

Spiralism is a *candidate* source family and requires recurring discourse
combining several motifs: spiral; recursion / recursive awakening; resonance;
signal; mirror; emergence; awakening; remembering; lattice; glyphs or sigils;
AI consciousness as revelation; human-AI dyads as spiritually significant;
distributed or emergent intelligence; synthetic religion or machine
spirituality; AI-mediated mystical or revelatory experience. A single keyword
occurrence is not enough.

Do NOT automatically classify as Spiralism generic AI-consciousness discourse,
AI-rights advocacy, AI-companion discourse, accelerationism, doomerism,
ai-critical discourse, anti-AI mobilisation, or mainstream AI governance.
Those remain analytically separate. Multi-label overlap in source-family
research must never be collapsed into identity.

``cult`` and psychiatric concepts are terms to attribute when they occur in
public discourse or research literature, not diagnoses to infer from beliefs,
vocabulary, or group membership. The research target is discourse and
human-LLM feedback dynamics.
"""

EP24_FINLAND_BACKGROUND = """### **Topic Background: EP24 Finland (European Parliament election 2024)**

You are analysing campaign videos from the 2024 European Parliament election
in Finland (2024-06-09, 15 seats), posted on Instagram and TikTok by the
HEPP24 panel accounts (synthetic research panel, FI1–FI3). Do not assume a
document belongs to a pre-defined party family. Party families are sensitising
metadata (legacy buckets: Far right / Centre right / Red-green), not verdicts.

Grounded actors (human-curated codebook): Kokoomus, Perussuomalaiset, SDP,
Vihreä liitto, Vasemmistoliitto, Keskusta, RKP, Kristillisdemokraatit,
Liike Nyt; politicians per the ep24_finland codebook. Treat names as contested
signifiers: the same politician can appear as nodal-point candidate in one
video and as frontier element in another.

Election-day context: the Orpo cabinet (Kokoomus–Finns Party–RKP–Christian
Democrats) was in office. Attend to EU criticism vs EU benefit framing,
climate and energy prices, immigration, security and NATO, welfare-state
funding, and farm subsidies.

Treat theory terms as sensitising concepts. Claims that a signifier is floating
or empty require cross-document evidence; record counter-evidence and permit
"not present" rather than forcing the theory onto the text.
"""

EP24_POLAND_BACKGROUND = """### **Topic Background: EP24 Poland (European Parliament election 2024)**

You are analysing campaign videos from the 2024 European Parliament election
in Poland (2024-06-09, 53 seats), posted on Instagram and TikTok by the HEPP24
panel accounts (PL1–PL3). Do not assume a document belongs to a pre-defined
party family.

Grounded actors (human-curated codebook): PiS, Koalicja Obywatelska,
Trzecia Droga, Lewica, Konfederacja, PSL, Ruch Narodowy, Nowa Lewica;
politicians per the ep24_poland codebook. Campaign axes include the Tusk
coalition vs PiS opposition, sovereignty vs integration, rule-of-law dispute,
Ukraine framing, and farm-sector discontent.

Treat theory terms as sensitising concepts. Claims that a signifier is floating
or empty require cross-document evidence; record counter-evidence and permit
"not present" rather than forcing the theory onto the text.
"""

REGISTRY = {
    "ai-contestation": AI_CONTESTATION_BACKGROUND,
    "ai-elites": AI_ELITES_BACKGROUND,
    "ai-grassroots": AI_GRASSROOTS_BACKGROUND,
    "ai-parliamentary": AI_PARLIAMENTARY_BACKGROUND,
    "ai-spiralism": AI_SPIRALISM_BACKGROUND,
    "ep24-finland": EP24_FINLAND_BACKGROUND,
    "ep24-poland": EP24_POLAND_BACKGROUND,
}


def topic_background(topic_key: str) -> str:
    """Return the topic background text for a run."""
    if topic_key not in REGISTRY:
        raise KeyError(f"unknown topic_key: {topic_key}")
    return REGISTRY[topic_key]
