"""Poll-of-polls: a reproducible, statistically explicit NFL power rankings
consensus built from multiple public weekly rankings.

Modules
-------
teams      canonical club identity and name resolution
fetch      cached HTTP retrieval of source pages
sources    one parser per publication, all rank-ordinal
validate   hard gate on ballot completeness and rank permutation
stats      standardisation, random-effects pooling, bootstrap uncertainty
report     rendered markdown report and site data bundle
"""

__all__ = ["teams", "fetch", "sources", "validate", "stats", "report"]
__version__ = "1.0.0"
