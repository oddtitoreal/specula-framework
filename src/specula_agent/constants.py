"""Canonical constants for the Specula runtime."""

PHASE_SEQUENCE = ("0", "1", "1.5", "2", "3", "4", "5", "6")

NEXT_PHASE = {
    "0": "1",
    "1": "1.5",
    "1.5": "2",
    "2": "3",
    "3": "4",
    "4": "5",
    "5": "6",
    "6": "1",
}

ALLOWED_MODES = {
    "exploration",
    "convergence",
    "brand_archaeology",
    "prototyping",
    "ethical_gate",
    "refusal_register",
    "narrative_synthesis",
    "community_cocreation",
    "guardian",
    "cognitive_sparring",
    "sensemaking",
    "slowdown",
    "refusal",
}

PHASE_DEFAULT_MODE = {
    "0": "sensemaking",
    "1": "exploration",
    "1.5": "convergence",
    "2": "brand_archaeology",
    "3": "prototyping",
    "4": "narrative_synthesis",
    "5": "community_cocreation",
    "6": "guardian",
}

FORBIDDEN_PHRASES = (
    "you should",
    "the best choice",
    "the correct option",
    "we recommend",
    "choose x",
)
