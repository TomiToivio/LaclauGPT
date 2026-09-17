# AC/DT backwards-compatibility fixtures

These are deliberately small, synthetic public fixtures for testing the compatibility contract in issue #36. They contain no private research data.

Each fixture is intended to survive the path:

`legacy import -> normalize -> analyse/load result -> export -> re-import -> visualize`

without losing source identity, provenance or methodological semantics.

Files:

- `manifesto_scaling_emotion.json`: Finnish-style manifesto scaling plus sentiment/emotion measurements.
- `tweet_peak_close_reading.json`: hashtag/tweet temporal peak plus selected primary records.
- `hashtag_ecosystem.json`: co-occurrence network with evidence links.
- `ep_actor_topic_sna.json`: EP-style actor/thematic/topic/SNA result.
- `multimodal_timecoded.json`: transcript/OCR/frame evidence with timestamps.
- `laclau_theoretical_output.json`: reviewed discourse-theoretical result demonstrating the stronger interpretation mode.

The synthetic content is not a political finding. The fixtures test software semantics only.