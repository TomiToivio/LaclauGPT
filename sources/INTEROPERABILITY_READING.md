# Interoperability and computational-method reading list

This reading list supports the cross-tool compatibility contract in `docs/CROSS_TOOL_COMPATIBILITY_CONTRACT.md`. It is a methodological bibliography, not a claim that any computational method is equivalent to Laclau/Mouffe/Palonen discourse theory.

## Laclau, Mouffe and discourse theory

- Laclau, Ernesto & Chantal Mouffe. *Hegemony and Socialist Strategy: Towards a Radical Democratic Politics*. Verso.
- Laclau, Ernesto. *On Populist Reason*. Verso, 2005.
- Palonen, Emilia. Relevant work on populism, polarisation, political frontiers and hegemony. See the project source summaries and paper bibliography for study-specific use.

## Computational social science and text as data

- Grimmer, Justin & Brandon M. Stewart (2013). “Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts.” *Political Analysis* 21(3): 267–297. DOI: https://doi.org/10.1093/pan/mps028
- Salganik, Matthew J. *Bit by Bit: Social Research in the Digital Age*. Princeton University Press.
- Lazer, David et al. (2009). “Computational Social Science.” *Science* 323(5915): 721–723. DOI: https://doi.org/10.1126/science.1167742
- Lazer, David M. J. et al. (2020). “Computational social science: Obstacles and opportunities.” *Science* 369(6507): 1060–1062. DOI: https://doi.org/10.1126/science.aaz8170

## Discourse Network Analysis

- Leifeld, Philip. Methodological work on Discourse Network Analysis, policy debates and dynamic actor-concept networks, together with the DNA and rDNA software documentation.
- DNA / rDNA documentation and associated peer-reviewed publications should be treated as the implementation reference for statement coding, network construction and longitudinal discourse-network analysis.

## Topic models and text representations

- Roberts, Margaret E.; Stewart, Brandon M.; Tingley, Dustin et al. Structural Topic Model papers, including the *Journal of Statistical Software* article “stm: An R Package for Structural Topic Models.” DOI: https://doi.org/10.18637/jss.v091.i02
- Bianchi, Federico; Terragni, Silvia; Hovy, Dirk (2021). “Pre-training is a Hot Topic: Contextualized Document Embeddings Improve Topic Coherence.” *ACL-IJCNLP 2021*. DOI: https://doi.org/10.18653/v1/2021.acl-short.96
- Grootendorst, Maarten (2022). “BERTopic: Neural topic modeling with a class-based TF-IDF procedure.” arXiv:2203.05794.
- Reimers, Nils & Iryna Gurevych (2019). “Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.” *EMNLP-IJCNLP 2019*. DOI: https://doi.org/10.18653/v1/D19-1410

## Networks

- Traag, Vincent A.; Waltman, Ludo; van Eck, Nees Jan (2019). “From Louvain to Leiden: guaranteeing well-connected communities.” *Scientific Reports* 9:5233. DOI: https://doi.org/10.1038/s41598-019-41695-z
- Newman, M. E. J. *Networks*. Oxford University Press.

## DATS and human-in-the-loop qualitative analysis

Use the DATS repository and publications as the primary implementation references for:

- Discourse Analysis Tool Suite architecture and data model;
- COTA / Concept-over-Time workflows;
- Annotation Assistant / human-in-the-loop coding;
- Whiteboards / visual qualitative workspaces.

LaclauGPT uses these as interoperability and methodological references. DATS categories remain researcher-defined analytical objects rather than theoretical ground truth.

## R and Python scientific ecosystems

- Benoit, Kenneth et al. (2018). “quanteda: An R package for the quantitative analysis of textual data.” *Journal of Open Source Software* 3(30): 774. DOI: https://doi.org/10.21105/joss.00774
- `stm`, `igraph`, `arrow`, `tidyverse`/`data.table` and `ggplot2` are initial R compatibility targets.
- Python-side compatibility includes standard tabular, NLP, embedding, network and statistical libraries used in the Analysis module. Scientific software papers should be cited where available when a library materially contributes to a published analysis.

## Interpretation rule

Computational outputs are evidence and analytical representations, not automatic discourse-theoretical conclusions. In particular, community detection is not automatically a formation, semantic similarity is not equivalence, negative sentiment is not antagonism, network degree is not nodal status, and topic prevalence is not hegemony. Any such theoretical interpretation must remain evidence-linked, explicit and human-reviewed.
