# SPECULA AI – SYSTEM ARCHITECTURE AND INPUT SPECIFICATIONS

This document provides a **formal, implementation-oriented specification** of the SPECULA AI system architecture, with a specific focus on **input requirements, AI processes, and phase-specific outputs**.

It complements *“SPECULA AI – JSON Schemas and Output Architecture”* and should be treated as its **normative counterpart for system design and training**.

In case of conflict, **output schemas take precedence over process descriptions**.

---

## 1. SYSTEM ARCHITECTURE OVERVIEW

### Two Possible Implementation Approaches

#### A. Prompt-Based System (Recommended for MVP)

* Uses existing LLMs (Claude / GPT-4)
* Relies on structured system prompts and phase guards
* No fine-tuning required
* Estimated setup time: **2–4 weeks**

#### B. Fine-Tuned Model (Enterprise / Production)

* Fine-tuned on SPECULA-specific datasets
* Requires 50–100 annotated conversations
* Higher cost and governance complexity
* Estimated training time: **2–3 months**

---

## 2. PHASED INPUT SPECIFICATIONS

### PHASE 0 – ACTIVATION

#### Required Input

```json
{
  "project_name": "string",
  "brand_name": "string",
  "sector": "string",
  "starting_phase": "1|2|3|4|5|6",
  "team_context": {
    "stakeholders": ["string"],
    "decision_authority": "string",
    "timeline": "string"
  }
}
```

#### AI Responsibilities

* Confirm activation
* Set conversational and project context
* Confirm starting phase

---

### PHASE 1 – SCENARIO GENERATION

#### Required Input

```json
{
  "sector": "string",
  "current_positioning": "string",
  "time_horizon": "5|10|20",
  "known_drivers": [
    {
      "type": "tech|cultural|economic|environmental|regulatory",
      "description": "string",
      "source": "string (optional)"
    }
  ],
  "constraints": {
    "geography": "string",
    "regulation": "string",
    "budget_range": "string"
  },
  "number_of_scenarios": "4–6"
}
```

#### AI Process

1. Analyze provided drivers
2. Enrich with weak signals (database / search)
3. Generate 4–6 scenarios (temperature 0.8–0.9)
4. Attach **one maieutic question per scenario**

#### Output (Aligned to Output Spec)

```json
{
  "scenarios": [
    {
      "id": "string",
      "name": "string",
      "drivers": ["string"],
      "description": "string",
      "type": "preferred|feared|wild_card|negative",
      "question": "string",
      "user_response": null
    }
  ]
}
```

---

### PHASE 1.5 – COMPETITIVE FUTURES MAPPING

#### Required Input

```json
{
  "competitors": [
    {
      "name": "string",
      "current_positioning": "string",
      "recent_investments": ["string"],
      "partnerships": ["string"],
      "public_statements": ["string"],
      "narrative_signals": ["string"]
    }
  ],
  "mapping_dimensions": ["string"]
}
```

#### AI Process

1. Score competitors across dimensions
2. Identify clusters and dominant trajectories
3. Detect white spaces
4. Suggest differentiation territories

#### Output

```json
{
  "competitive_map": [
    {
      "competitor": "string",
      "future_trajectory": "string",
      "occupied_territory": "string",
      "ignored_territories": ["string"]
    }
  ],
  "white_spaces": [
    {
      "id": "string",
      "description": "string",
      "why_empty": "string",
      "alignment_with_brand": "low|medium|high"
    }
  ],
  "recommended_territory": "string"
}
```

---

### PHASE 2 – BRAND ARCHAEOLOGY

#### Required Input

```json
{
  "brand_materials": {
    "mission_vision": "string",
    "past_decisions": [
      {
        "decision": "string",
        "context": "string",
        "outcome": "string",
        "year": "number"
      }
    ],
    "communication_history": ["string"],
    "product_evolution": ["string"],
    "crises_managed": [
      {
        "crisis": "string",
        "response": "string",
        "values_tested": ["string"]
      }
    ]
  },
  "stakeholder_interviews": [
    {
      "role": "string",
      "transcript": "string"
    }
  ]
}
```

#### AI Process

* NLP analysis on materials
* Progressive identity questioning
* Identification of contradictions
* Refusal of vague answers

#### Output

```json
{
  "brand_dna": { ... },
  "archaeology_transcript": "string"
}
```

---

### PHASE 3 – PROTOTYPING + ETHICAL GATE

#### Required Input

```json
{
  "scenarios": "from Phase 1",
  "brand_dna": "from Phase 2",
  "prototypes_to_generate": "3–5",
  "stress_test_scenarios": ["string"]
}
```

#### AI Process

* Generate prototypes per scenario
* Apply stress tests
* Run Ethical Gate (formal checks)
* Register refusals

#### Output

```json
{
  "prototypes": [ ... ],
  "registry_of_refusals": [ ... ]
}
```

---

### PHASE 4 – NARRATIVE SYNTHESIS

#### Required Input

```json
{
  "validated_prototypes": "from Phase 3",
  "brand_dna": "from Phase 2",
  "registry_of_refusals": "from Phase 3",
  "scenarios": "from Phase 1"
}
```

#### AI Process

* Extract meta-narrative
* Build adaptive storylines
* Define dynamic narrative rules

#### Output

```json
{
  "narrative_system": { ... }
}
```

---

### PHASE 5 – COMMUNITY CO-CREATION

#### Required Input

```json
{
  "narrative_system": "from Phase 4",
  "brand_dna": "from Phase 2",
  "community_segments": [ ... ],
  "co_creation_format": "string",
  "negotiable_elements": ["string"],
  "non_negotiable_elements": ["string"]
}
```

#### AI Process

* Facilitate dialogue
* Aggregate large-scale input
* Detect consensus and divergence
* Preserve radical values

#### Output

```json
{
  "co_creation_insights": { ... },
  "updated_narrative_system": { ... }
}
```

---

### PHASE 6 – SPECULA GUARDIAN

#### Required Input (Quarterly)

```json
{
  "brand_dna": "from Phase 2",
  "scenarios": "from Phase 1",
  "narrative_system": "from Phase 4",
  "registry_of_refusals": "from Phase 3",
  "current_signals": [ ... ],
  "current_kpis": { ... },
  "decisions_log": [ ... ]
}
```

#### AI Process

* Compare signals vs scenarios
* Classify divergence
* Monitor behavioral coherence
* Trigger re-speculation if needed

#### Output

```json
{
  "guardian_report": { ... },
  "re_speculation_triggered": "boolean"
}
```

---

## 3. TRAINING DATASET REQUIREMENTS (FINE-TUNING)

### Minimum Viable Dataset

```
- 50–100 annotated conversations
- 30 speculative scenarios
- 20 documented brand DNAs
- 50 prototypes with ethical evaluations
- 30 adaptive narratives
- 10 full Guardian cycles
```

### Annotation Schema

```json
{
  "conversation_id": "string",
  "phase": "1|2|3|4|5|6",
  "turns": [
    {
      "role": "user|assistant",
      "content": "string",
      "cognitive_mode": "divergent|convergent|evaluative|maieutic",
      "quality_score": "1–5",
      "annotations": { ... }
    }
  ]
}
```

---

## 4. TECHNICAL INFRASTRUCTURE

```yaml
LLM:
  - Claude Sonnet / GPT-4
Vector DB:
  - Pinecone / Weaviate
Databases:
  - PostgreSQL
Cache:
  - Redis
Orchestration:
  - LangChain / LlamaIndex
API:
  - FastAPI
Frontend:
  - React (Guardian Dashboard)
```

---

## 5. STORAGE STRUCTURE

```text
projects/
  └── {project_id}/
      ├── brand_dna.json
      ├── scenarios.json
      ├── prototypes.json
      ├── registry_refusals.json
      ├── narrative_system.json
      └── guardian_reports/
          ├── 2026_Q1.json
          └── 2026_Q2.json
```

---

**SPECULA AI – System Architecture and Input Specifications**
Version 1.0
