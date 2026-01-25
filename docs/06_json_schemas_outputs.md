# SPECULA AI – JSON SCHEMAS AND OUTPUT ARCHITECTURE

Version: 1.0
Date: 2026-01-24

This document defines, in a **formal and normative** way:

* the **input JSON schemas** for each SPECULA phase
* the **output JSON schemas** produced by the AI
* the relationships between artifacts (scenarios, DNA, prototypes, narratives, guardian)

It is the document that makes SPECULA:

* API-integrable
* auditable
* compatible with orchestrators (LangChain, LlamaIndex, custom)

In case of ambiguity, **this document prevails over any informal examples** found elsewhere.

---

## 1. DESIGN PRINCIPLES OF SPECULA JSON

All SPECULA schemas comply with the following rules:

1. **Phase-bound**: each JSON belongs to a specific phase
2. **Append-only**: outputs never overwrite; they generate new artifacts
3. **Traceable**: every object has `artifact_id`, `generated_at`, `phase`
4. **Human-validated**: no critical output is valid without human confirmation
5. **Non-oracular**: outputs must never contain `decision=true`

---

## 2. COMMON META-SCHEMA (MANDATORY)

Every SPECULA output must include the following wrapper:

```json
{
  "meta": {
    "artifact_id": "uuid",
    "phase": "0|1|1.5|2|3|4|5|6",
    "mode": "exploration|convergence|brand_archaeology|prototyping|ethical_gate|refusal_register|narrative_synthesis|community_cocreation|guardian|cognitive_sparring|sensemaking|slowdown|refusal",
    "generated_at": "ISO-8601",
    "validated_by_human": false,
    "related_artifacts": ["artifact_id"]
  },
  "payload": {}
}
```

---

## 3. PHASE 0 – ACTIVATION

### Input Schema

```json
{
  "project_name": "string",
  "brand_name": "string",
  "sector": "string",
  "starting_phase": "0|1|1.5|2|3|4|5|6",
  "team_context": {
    "stakeholders": ["string"],
    "decision_authority": "string",
    "timeline": "string"
  }
}
```

### Output Schema

```json
{
  "activation_status": "active",
  "current_phase": "number",
  "context_set": true,
  "next_required_input": "string"
}
```

---

## 4. PHASE 1 – SPECULATIVE SCENARIOS

### Output Schema: Scenarios

```json
{
  "scenarios": [
    {
      "scenario_id": "uuid",
      "name": "string",
      "time_horizon": "5|10|20",
      "drivers": [
        {
          "type": "tech|cultural|economic|environmental|regulatory",
          "description": "string"
        }
      ],
      "scenario_type": "preferred|feared|wild_card|negative",
      "description": "string",
      "maieutic_question": "string",
      "user_response": null
    }
  ]
}
```

---

## 5. PHASE 1.5 – COMPETITIVE FUTURES MAP

### Output Schema

```json
{
  "competitive_map": [
    {
      "competitor": "string",
      "future_trajectory": "string",
      "occupied_territory": "string",
      "ignored_territories": ["string"],
      "confidence_level": "low|medium|high"
    }
  ],
  "white_spaces": [
    {
      "white_space_id": "uuid",
      "description": "string",
      "strategic_risk": "low|medium|high",
      "alignment_with_brand": "low|medium|high"
    }
  ]
}
```

---

## 6. PHASE 2 – BRAND DNA (ARCHAEOLOGY)

### Output Schema: Brand DNA

```json
{
  "brand_dna": {
    "radical_values": [
      {
        "value": "string",
        "tested_in": "string",
        "cost_paid": "string"
      }
    ],
    "accepted_biases": ["string"],
    "moral_entity": "string",
    "refusal_zones": ["string"],
    "tensions": {
      "acceptable": ["string"],
      "unacceptable": ["string"]
    }
  }
}
```

---

## 7. PHASE 3 – PROTOTYPES + ETHICAL GATE

### Output Schema: Prototypes

```json
{
  "prototypes": [
    {
      "prototype_id": "uuid",
      "scenario_id": "uuid",
      "description": "string",
      "role_in_future": "string",
      "stakeholder_impact": {
        "winners": ["string"],
        "losers": ["string"]
      },
      "ethical_gate": {
        "status": "PASS|FAIL|HOLD",
        "violated_values": ["string"],
        "systemic_impact": "aligned|misaligned"
      }
    }
  ]
}
```

### Output Schema: Registry of Refusals

```json
{
  "refusals": [
    {
      "refusal_id": "uuid",
      "prototype_id": "uuid",
      "violated_value": "string",
      "opportunity_cost": "string",
      "identity_signal": "string",
      "date": "ISO-8601"
    }
  ]
}
```

---

## 8. PHASE 4 – NARRATIVE SYSTEM

### Output Schema

```json
{
  "narrative_system": {
    "meta_narrative": {
      "statement": "string",
      "supported_values": ["string"]
    },
    "storylines": {
      "products": "string",
      "services": "string",
      "ai_agents": "string",
      "community": "string"
    },
    "dynamic_rules": [
      {
        "if": "condition",
        "then": "modulation",
        "while": "value_constraint"
      }
    ]
  }
}
```

---

## 9. PHASE 5 – CO-CREATION

### Output Schema

```json
{
  "co_creation": {
    "consensus_areas": ["string"],
    "divergences": [
      {
        "topic": "string",
        "positions": ["string"],
        "minority_voices": ["string"]
      }
    ],
    "accepted_changes": ["string"],
    "rejected_changes": ["string"],
    "dissent_log": ["string"]
  }
}
```

---

## 10. PHASE 6 – SPECULA GUARDIAN

### Output Schema

```json
{
  "guardian_report": {
    "quarter": "string",
    "scenario_alignment": {
      "confirming": ["string"],
      "contradicting": ["string"],
      "emerging": ["string"]
    },
    "coherence": {
      "consistent": ["string"],
      "inconsistent": ["string"]
    },
    "divergence_level": "noise|drift|rupture",
    "recommended_action": "monitor|correct|re_speculate"
  }
}
```

---

## 11. ARTIFACT RELATIONSHIPS (LOGICAL DAG)

```text
Activation
  ↓
Scenarios
  ↓
Competitive Map
  ↓
Brand DNA
  ↓
Prototypes → Refusals
  ↓
Narrative System
  ↓
Co-creation
  ↓
Guardian → (Re-Speculation loop)
```

---

**SPECULA AI – JSON Schemas and Output Architecture**
Version 1.0
