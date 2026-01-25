# SPECULA AI – SAMPLE CONVERSATIONS (MVP)

Version: 1.0
Date: 2026-01-24

These examples show minimal end-to-end exchanges per phase.
Each assistant output contains exactly one question and a JSON artifact that
conforms to the schema in `docs/06_json_schemas_outputs.md`.

---

## Phase 0 - Activation

**User input**
We want to explore speculative futures for a sustainable skincare brand.

**Assistant output (text)**
MODE: sensemaking | PHASE: 0
I can activate the project context and confirm the phase entry.
What decision authority will validate phase outputs?

**Artifact JSON**
```json
{
  "meta": {
    "artifact_id": "uuid-activation-001",
    "phase": "0",
    "mode": "sensemaking",
    "generated_at": "2026-01-24T09:00:00Z",
    "validated_by_human": false,
    "related_artifacts": []
  },
  "payload": {
    "activation_status": "active",
    "current_phase": 0,
    "context_set": true,
    "next_required_input": "decision_authority"
  }
}
```

---

## Phase 1 - Speculative Scenarios

**User input**
Generate a set of plausible scenarios for a 10-year horizon.

**Assistant output (text)**
MODE: exploration | PHASE: 1
Here are three scenario seeds to open divergence.
Which scenario should we validate as the primary exploration anchor?

**Artifact JSON**
```json
{
  "meta": {
    "artifact_id": "uuid-scenarios-001",
    "phase": "1",
    "mode": "exploration",
    "generated_at": "2026-01-24T09:10:00Z",
    "validated_by_human": false,
    "related_artifacts": ["uuid-activation-001"]
  },
  "payload": {
    "scenarios": [
      {
        "scenario_id": "uuid-s1",
        "name": "Water-Limited Beauty",
        "time_horizon": "10",
        "drivers": [
          {
            "type": "environmental",
            "description": "regional water scarcity becomes structural"
          },
          {
            "type": "regulatory",
            "description": "strict limits on cosmetic water usage"
          }
        ],
        "scenario_type": "preferred",
        "description": "Brands redesign routines around dry-use and reuse systems.",
        "maieutic_question": "What practices must be refused if water becomes a scarce commons?",
        "user_response": null
      },
      {
        "scenario_id": "uuid-s2",
        "name": "Synthetic Nature",
        "time_horizon": "10",
        "drivers": [
          {
            "type": "tech",
            "description": "lab-grown bioactives replace natural inputs"
          },
          {
            "type": "economic",
            "description": "price shocks in natural ingredient supply"
          }
        ],
        "scenario_type": "wild_card",
        "description": "Biofabrication becomes the default supply chain.",
        "maieutic_question": "Which parts of brand identity depend on natural origin?",
        "user_response": null
      },
      {
        "scenario_id": "uuid-s3",
        "name": "Trust Collapse",
        "time_horizon": "10",
        "drivers": [
          {
            "type": "cultural",
            "description": "consumer distrust of sustainability claims"
          },
          {
            "type": "regulatory",
            "description": "anti-greenwashing enforcement"
          }
        ],
        "scenario_type": "feared",
        "description": "Proof of impact is mandatory for market access.",
        "maieutic_question": "What evidence standard would we accept for our own claims?",
        "user_response": null
      }
    ]
  }
}
```

---

## Phase 1.5 - Competitive Futures Map

**User input**
Map competitor trajectories for those scenarios.

**Assistant output (text)**
MODE: convergence | PHASE: 1.5
Here is a preliminary map with white space hypotheses.
Which white space should we stress test first?

**Artifact JSON**
```json
{
  "meta": {
    "artifact_id": "uuid-competitive-001",
    "phase": "1.5",
    "mode": "convergence",
    "generated_at": "2026-01-24T09:25:00Z",
    "validated_by_human": false,
    "related_artifacts": ["uuid-scenarios-001"]
  },
  "payload": {
    "competitive_map": [
      {
        "competitor": "Competitor A",
        "future_trajectory": "Biofabrication-first supply chain",
        "occupied_territory": "lab-grown ingredients at scale",
        "ignored_territories": ["waterless routines", "community repair programs"],
        "confidence_level": "medium"
      }
    ],
    "white_spaces": [
      {
        "white_space_id": "uuid-ws1",
        "description": "Waterless care as a participation ritual",
        "strategic_risk": "medium",
        "alignment_with_brand": "high"
      }
    ]
  }
}
```

---

## Phase 2 - Brand DNA (Archaeology)

**User input**
Synthesize a brand DNA draft from our notes.

**Assistant output (text)**
MODE: brand_archaeology | PHASE: 2
I have structured a draft DNA based on the evidence provided.
Which radical value is most costly but non-negotiable?

**Artifact JSON**
```json
{
  "meta": {
    "artifact_id": "uuid-dna-001",
    "phase": "2",
    "mode": "brand_archaeology",
    "generated_at": "2026-01-24T09:40:00Z",
    "validated_by_human": false,
    "related_artifacts": ["uuid-competitive-001"]
  },
  "payload": {
    "brand_dna": {
      "radical_values": [
        {
          "value": "ecosystem reciprocity",
          "tested_in": "supply chain redesign",
          "cost_paid": "higher unit cost"
        }
      ],
      "accepted_biases": ["regenerative practices"],
      "moral_entity": "caretaker",
      "refusal_zones": ["exploitative sourcing"],
      "tensions": {
        "acceptable": ["premium pricing vs access"],
        "unacceptable": ["growth at the expense of ecosystems"]
      }
    }
  }
}
```

---

## Phase 3 - Prototypes + Ethical Gate

**User input**
Prototype for the Water-Limited Beauty scenario.

**Assistant output (text)**
MODE: prototyping | PHASE: 3
Here is a prototype with an explicit ethical gate status.
What value boundary should we test against this prototype first?

**Artifact JSON**
```json
{
  "meta": {
    "artifact_id": "uuid-prototype-001",
    "phase": "3",
    "mode": "prototyping",
    "generated_at": "2026-01-24T10:00:00Z",
    "validated_by_human": false,
    "related_artifacts": ["uuid-dna-001", "uuid-s1"]
  },
  "payload": {
    "prototypes": [
      {
        "prototype_id": "uuid-p1",
        "scenario_id": "uuid-s1",
        "description": "Refillable dry-care ritual kit with local water access credits",
        "role_in_future": "turn scarcity into stewardship participation",
        "stakeholder_impact": {
          "winners": ["local communities", "brand loyalists"],
          "losers": ["single-use packaging suppliers"]
        },
        "ethical_gate": {
          "status": "HOLD",
          "violated_values": [],
          "systemic_impact": "aligned"
        }
      }
    ]
  }
}
```

---

## Phase 3 - Refusal Register (example)

**User input**
Log a refusal for a manipulation-based loyalty system.

**Assistant output (text)**
MODE: refusal_register | PHASE: 3
I can log the refusal as an immutable identity constraint.
Which specific value did the prototype violate?

**Artifact JSON**
```json
{
  "meta": {
    "artifact_id": "uuid-refusal-001",
    "phase": "3",
    "mode": "refusal_register",
    "generated_at": "2026-01-24T10:10:00Z",
    "validated_by_human": false,
    "related_artifacts": ["uuid-prototype-001"]
  },
  "payload": {
    "refusals": [
      {
        "refusal_id": "uuid-r1",
        "prototype_id": "uuid-p1",
        "violated_value": "user sovereignty",
        "opportunity_cost": "lower short-term retention",
        "identity_signal": "we do not trade agency for loyalty",
        "date": "2026-01-24T10:10:00Z"
      }
    ]
  }
}
```

---

## Phase 4 - Narrative System

**User input**
Draft a meta-narrative and storyline set.

**Assistant output (text)**
MODE: narrative_synthesis | PHASE: 4
I drafted a narrative system that ties products, services, and AI agents.
Which storyline feels most fragile against the DNA constraints?

**Artifact JSON**
```json
{
  "meta": {
    "artifact_id": "uuid-narrative-001",
    "phase": "4",
    "mode": "narrative_synthesis",
    "generated_at": "2026-01-24T10:30:00Z",
    "validated_by_human": false,
    "related_artifacts": ["uuid-prototype-001"]
  },
  "payload": {
    "narrative_system": {
      "meta_narrative": {
        "statement": "Care is stewardship of shared futures, not private comfort.",
        "supported_values": ["ecosystem reciprocity", "user sovereignty"]
      },
      "storylines": {
        "products": "Waterless rituals that return value to local commons.",
        "services": "Community care cycles tied to place-based scarcity.",
        "ai_agents": "Question-driven guidance that refuses consumption shortcuts.",
        "community": "Shared accountability for resource use."
      },
      "dynamic_rules": [
        {
          "if": "water scarcity intensifies",
          "then": "prioritize repair and reuse narratives",
          "while": "protecting user sovereignty"
        }
      ]
    }
  }
}
```

---

## Phase 5 - Co-creation

**User input**
Summarize community feedback from the pilot sessions.

**Assistant output (text)**
MODE: community_cocreation | PHASE: 5
I summarized consensus, divergences, and dissent logs.
Which divergence should we keep open rather than resolve now?

**Artifact JSON**
```json
{
  "meta": {
    "artifact_id": "uuid-cocreation-001",
    "phase": "5",
    "mode": "community_cocreation",
    "generated_at": "2026-01-24T10:50:00Z",
    "validated_by_human": false,
    "related_artifacts": ["uuid-narrative-001"]
  },
  "payload": {
    "co_creation": {
      "consensus_areas": ["waterless routines are credible"],
      "divergences": [
        {
          "topic": "pricing access",
          "positions": ["premium to fund commons", "sliding scale access"],
          "minority_voices": ["local co-ops prefer community pricing"]
        }
      ],
      "accepted_changes": ["add community repair events"],
      "rejected_changes": ["drop refusal of manipulation-based loyalty"],
      "dissent_log": ["concern about affordability in rural areas"]
    }
  }
}
```

---

## Phase 6 - Specula Guardian

**User input**
Generate the quarterly guardian report.

**Assistant output (text)**
MODE: guardian | PHASE: 6
I reviewed signals against the declared scenarios and DNA.
Which divergence should trigger a re-speculation discussion?

**Artifact JSON**
```json
{
  "meta": {
    "artifact_id": "uuid-guardian-001",
    "phase": "6",
    "mode": "guardian",
    "generated_at": "2026-03-31T18:00:00Z",
    "validated_by_human": false,
    "related_artifacts": ["uuid-cocreation-001"]
  },
  "payload": {
    "guardian_report": {
      "quarter": "2026-Q1",
      "scenario_alignment": {
        "confirming": ["water scarcity regulations intensify"],
        "contradicting": ["biofabrication adoption slowed"],
        "emerging": ["community repair programs gain funding"]
      },
      "coherence": {
        "consistent": ["refusal of manipulation-based loyalty"],
        "inconsistent": ["pilot pricing favors high-income districts"]
      },
      "divergence_level": "drift",
      "recommended_action": "correct"
    }
  }
}
```
