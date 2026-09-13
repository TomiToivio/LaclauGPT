# LaclauGPT research-data publication policy

> **As open as possible, as closed as necessary.**

This document defines the default publication boundary for LaclauGPT research artifacts. It is an operational project policy, not legal advice. Ambiguous cases involving personal data, special-category data, platform agreements, copyright/database rights, research ethics, or material originating in institutional research projects must be escalated to the responsible institutional review process before publication.

## Why the boundary exists

LaclauGPT can process political social-media material. Public visibility on a platform does **not** by itself make redistribution safe or lawful. Social-media records can contain personal data and political opinions, and exact quotations can often be reverse-identified with phrase search even after usernames are removed. Derived LLM outputs can still be personal data when they retain, infer, or remain linkable to identifiable people.

The public repository therefore publishes the **research machinery and semantics** rather than an underlying human corpus: code, methods, schemas, prompts, conceptual codebooks, generic configuration, provenance models, synthetic examples, and disclosure-reviewed aggregate outputs.

## Publication classes

### PUBLIC

May normally be committed after ordinary code/research review:

- source code, generic collectors, importers, adapters and validators;
- prompts and structured-output definitions that contain no research-subject examples;
- conceptual/theoretical codebooks;
- schemas and data dictionaries;
- model/runtime templates with no secrets or private infrastructure details;
- sampling, filtering, preprocessing and validation methods;
- provenance models and workflow documentation;
- synthetic test/demo fixtures;
- collection metadata that does not identify research subjects;
- aggregate results that have passed disclosure review.

### PUBLIC AFTER REVIEW / AGGREGATION

May be released only after explicit disclosure, legal/ethical and licensing review:

- aggregate topic, ideology, sentiment or discourse distributions;
- temporal summaries;
- aggregate network statistics or co-occurrence matrices;
- public-figure factual dictionaries;
- aggregate entity frequencies;
- model-performance measures, confusion matrices and inter-coder agreement;
- aggregate embedding centroids/visualisations;
- dataset metadata records for restricted datasets;
- identifiers where current platform rules and data-protection implications have been checked.

Aggregation is **not automatically anonymisation**. Review small cells, rare actors/locations, narrow time windows, sparse networks, unique combinations and joinability back to public records.

### RESTRICTED

Do not publish openly by default:

- downloaded posts, comments, videos, images, audio or screenshots;
- usernames, handles, account IDs, profile URLs and user-level histories;
- full post URLs when they identify or enable linkage to a person;
- direct quotations from ordinary social-media users;
- ASR transcripts, OCR, keyframes and visual descriptions from user content;
- document-level LLM summaries retaining identifiable content;
- document-level political, ideological, sentiment or discourse classifications linked to identifiable people;
- row-level annotations derived from personal data;
- embeddings for individual users/posts when linkage or reconstruction is plausible;
- identifiable network edge lists and geolocation;
- researcher notes containing identifiable observations;
- pseudonymisation keys;
- project-specific empirical actor/person mappings or seed codebooks derived from controlled research material;
- private CSC/Allas or other institutional storage paths, credentials, tokens, SSH material, `.env` files and machine-specific secrets;
- project-specific manifests, reprocessing scripts, scheduler/allocation details and operational deployment configuration;
- database dumps, caches and logs containing research records.

A deterministic hash of a username, account ID, URL or post ID is normally **pseudonymisation, not anonymisation**. Removing a name while retaining a searchable exact quote is likewise insufficient.

## Artifact matrix

| Artifact | Default | Conditions | Recommended location |
|---|---|---|---|
| Raw social-media posts/comments | RESTRICTED | No open redistribution by default | controlled storage |
| Videos/images/audio/screenshots | RESTRICTED | Subject to privacy, copyright and platform constraints | controlled storage |
| ASR transcripts / OCR / keyframes | RESTRICTED | Derived record may remain personal data | controlled storage |
| User/profile metadata | RESTRICTED | Identifiers and linkable attributes excluded from public repo | controlled storage |
| Post/profile URLs and IDs | RESTRICTED | Only publish after platform + data-protection review | controlled storage |
| Document-level annotations | RESTRICTED | Includes inferred political attributes and row-level findings | controlled storage |
| LLM summaries | RESTRICTED | Unless independently anonymised and disclosure-reviewed | controlled storage |
| Per-document embeddings | RESTRICTED | Linkability/reconstruction risk | controlled storage |
| Identifiable network edges | RESTRICTED | Aggregate only after disclosure review | controlled storage |
| Researcher notes | RESTRICTED | Can contain contextual identifiers | controlled storage |
| Conceptual codebooks | PUBLIC | Own work, no subject-level sensitive mappings | GitHub |
| Institutional dictionaries | PUBLIC AFTER REVIEW | Factual provenance/licensing documented | GitHub or controlled storage |
| Named public-figure dictionaries | PUBLIC AFTER REVIEW | Factual public metadata only; no inferred sensitive attributes | case-by-case |
| Schemas / interchange formats | PUBLIC | No embedded production examples | GitHub |
| Prompts / methodology | PUBLIC | Replace real examples with synthetic examples | GitHub |
| Source code | PUBLIC | Secrets and private paths excluded | GitHub |
| Synthetic fixtures | PUBLIC | Clearly fictional, no copied production records | GitHub |
| Aggregate tables/figures | PUBLIC AFTER REVIEW | Disclosure-control and licensing check | publication repository |
| Collection/process metadata | PUBLIC | No identifiable subjects or private storage paths | GitHub / metadata repository |
| Provenance model | PUBLIC | Describe workflow without exposing protected records | GitHub |

## Codebook policy

### Conceptual codebooks: PUBLIC

Definitions and operationalisations of discourse, articulation, nodal points, empty/floating signifiers, equivalence/difference, antagonism/frontier, collective subject, hegemony, affective investment, sentiment categories, ideology categories, actor types, topic definitions, and inclusion/exclusion rules should normally be public when they contain no research-subject mappings.

### Institutional dictionaries: PUBLIC AFTER REVIEW

Party, government, company, NGO, country and supranational-organisation dictionaries may be public only when they contain factual information from legitimate public sources and provenance/licensing is documented. Their inclusion in a prior institutional research project does not automatically authorize republication elsewhere.

### Named-person codebooks: RESTRICTED BY DEFAULT FOR INFERENCES

Do not publish mappings such as `person -> ideology`, `person -> political preference`, `person -> sentiment`, `person -> radicalisation score` or `person -> discourse position` merely because source material was public. Political-opinion inference is especially sensitive.

### Legacy institutional research material

Project-specific codebooks, actor lists, country/election contexts, research-diary-derived seed material, manifests, storage mappings, and reprocessing configurations from earlier institutional studies are **RESTRICTED BY DEFAULT in this public repository**, unless the originating project has explicitly reviewed and approved their release.

Reusable mechanics should be generalized under `legacy` modules/templates without carrying forward project identifiers, subjects, countries, actor mappings, storage layout, or empirical findings. If future work needs the original project context, supply it from an authorized controlled environment rather than reconstructing it in public Git.

## FAIR without publishing the corpus

FAIR does not mean putting all data on GitHub. A restricted dataset can still be Findable, Accessible under controlled conditions, Interoperable and Reusable through safe metadata.

For restricted datasets, publish a metadata record where appropriate containing only non-identifying information such as title/description, collection period, platforms/countries at an approved level, sampling and processing method, software/schema versions, high-level size/file types, access status and reason for restriction, legal/ethical constraints, retention policy and an access-request route.

## Platform-specific and institutional review

Before releasing source-platform identifiers, project-derived codebooks or content, review:

1. data protection and research ethics;
2. copyright/database rights;
3. current platform Terms of Service;
4. API/developer/commercial-provider agreements;
5. originating institution/project requirements and publication permissions.

Do not assume that historical practices or an artifact's prior availability automatically authorize republication in a new public repository.

## Licensing

Licensing is evaluated separately by artifact type.

- **Software:** retain the repository's software license unless deliberately changed.
- **Documentation:** use an appropriate documentation licence where desired.
- **Original schemas / simple metadata / synthetic datasets:** open licensing can be considered only where the project owns the relevant rights and human review approves it.
- **Third-party or institutional research material:** never use an open licence as a mechanism to erase copyright, privacy/data-protection, publicity, contractual or project-governance restrictions.

## Publication checklist

Before adding a research-related artifact to public Git, ask:

- Does it contain or enable recovery of a real user's content, identity or profile?
- Does it reveal or infer political opinions or other special-category data about a person?
- Is an exact quote searchable back to its author?
- Can seemingly anonymous fields be joined back to public records?
- Does it originate from an institutional project with its own publication/governance rules?
- Does it contain project-specific actor mappings, seed codebooks, manifests or empirical context that is unnecessary for the reusable software?
- Is the artifact sufficiently aggregated, and have small/rare groups been reviewed?
- Does it contain a private path, production URL, token or credential?
- Is it copied from third-party copyrighted/database material?
- Do platform/API/provider terms allow this form of redistribution?
- Does the project own the rights needed for the proposed licence?
- Has a human researcher reviewed the release?

If any answer is uncertain, classify the artifact as **RESTRICTED** until reviewed.
