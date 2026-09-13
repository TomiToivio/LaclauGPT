# -*- coding: utf-8 -*-
"""Deprecated compatibility shim for a removed institutional research adapter.

Project-specific manifests, storage integration, identifiers and fetch logic are
not published in the public repository. Reusable acquisition functionality
belongs in the generic collectors and authorized legacy integrations should be
maintained outside the public tree.
"""

raise RuntimeError(
    "This project-specific adapter has been retired from the public repository. "
    "Use generic collector interfaces or an authorized legacy integration."
)
