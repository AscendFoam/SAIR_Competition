from __future__ import annotations


ERROR_TAXONOMY = {
    "FORMAT": "Output cannot be parsed as a strict boolean token.",
    "RULE_MISSING": "The prompt lacks a rule that appears needed for the case.",
    "RULE_CONFLICT": "Prompt rules appear to conflict or overfit.",
    "PROMPT_AMBIGUOUS": "The instruction order or wording allows multiple interpretations.",
    "FALSE_FILTER_WEAK": "The prompt is too eager to output true on non-implication cases.",
    "OVERCOMPRESSION": "Compression likely made the rule text hard for the model to interpret.",
    "MODEL_SPECIFIC": "The failure seems tied to one proxy model family.",
    "HARD_COMPOSITION": "The case appears to require multiple interacting rules.",
}

