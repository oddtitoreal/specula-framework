# Basic Case: Community Library Governance

This example walks through a complete SPECULA journey for a community library seeking to formalize governance around collection curation and community voice.

**Scenario:** A mid-sized public library (serving ~50,000 people) wants to shift from informal consensus to explicit democratic governance. The library has experienced conflict over collection decisions and wants to build a governance model that protects intellectual freedom while genuinely incorporating community input.

## The Journey: Phase 0 → Phase 6

### Phase 0: Activation
**File:** `phase-0-activation.json`

The library formally enters the SPECULA process. Key decision: This is not a small tweak—it's a commitment to systematic governance design.

**What happens:**
- Library board acknowledges the need for formalized governance
- Community survey confirms there's appetite for more voice in decisions
- Decision made: Let's design this carefully, informed by possible futures

**Output:** Activation status, confirmation of community readiness, clear signal that we're entering a 6-phase journey

---

### Phase 1: Scenarios
**File:** `phase-1-scenarios.json`

The library explores four possible futures across 10 years:

1. **Civic Hub (Preferred):** Library becomes true community center; stable funding; hybrid physical/digital thrives
2. **Irrelevance (Feared):** Budget cuts; digital replaces physical; library marginalized
3. **Hyperlocal Powerhouse (Wild Card):** Backlash against corporate platforms; library becomes hub of community-controlled network
4. **Politicized & Captured (Negative):** Library becomes battleground; independence lost; community loses trust

**Why this matters:**
Each scenario reveals what governance structure would be needed to thrive OR survive in that future. The "Civic Hub" scenario shows what we want. The "Politicized" scenario shows what we must guard against.

**Output:** Four tested scenarios; implicit governance requirements for each

---

### Phase 1.5: Competitive Map
**File:** `phase-1.5-competitive-map.json`

The library maps how it competes with (and differs from) alternatives:
- **Digital commerce** (Amazon, Google): Instant, personalized, infinite—but soulless, algorithm-driven
- **Commercial bookstores**: Curated, aesthetic, social—but expensive and profit-driven
- **Parks & civic spaces**: Free, accessible, community—but lack intellectual infrastructure

**Why this matters:**
The library's competitive advantage is NOT speed or convenience (we'll lose that). It's community, human curation, intellectual freedom, equity, and trust. Governance must protect these.

**Output:** Clear differentiation; understanding of what we protect and what we don't compete on

---

### Phase 2: Brand DNA
**File:** `phase-2-brand-dna.json`

The library articulates its essential identity:

**Core Values:**
1. **Intellectual Freedom** — Protection from censorship and algorithmic control
2. **Equity & Access** — Free for everyone; materials for all abilities
3. **Community Voice** — Governed by and accountable to people we serve
4. **Serendipity & Discovery** — Human curation; unexpected encounters

**Brand Archetype:** The Mentor/Sage + The Everyman

**Why this matters:**
These four values will guide every governance decision going forward. They create accountability. If later we're tempted to compromise (e.g., "Censor this controversial title"), we can test against our DNA: "Violates Intellectual Freedom value? Refused."

**Output:** Explicit, written values; clear identity that stakeholders understand

---

### Phase 3: Prototypes & Refusals
**File:** `phase-3-prototypes.json` + `phase-3-refusals.json`

The library tests three governance prototypes:
1. **Delegated Curation:** Librarians decide; community advises
2. **Participatory Curation:** Community votes on contested titles
3. **Algorithmic Curation:** Open-source tools assist; community retains override

AND specifies what we refuse to do:
- **Refuse censorship** — No removal of books for ideology (from any direction)
- **Refuse corporate algorithms** — No Google/Amazon/Apple curation
- **Refuse user surveillance** — No profiling or monetizing patron data
- **Refuse unequal access** — No tiered collections based on ability to pay

**Why this matters:**
Prototypes let us learn which governance model feels right *before* we commit. Refusals are our values made concrete: "If we're pressured to X, here's why we say no."

**Output:** Three tested models; explicit boundaries that protect identity

---

### Phase 4: Narrative System
**File:** `phase-4-narrative.json`

The library translates its identity into language that resonates with different audiences:

- **For patrons:** "Your library. Your voice shapes our decisions."
- **For city council:** "Cost-effective civic institution that builds social cohesion."
- **For donors:** "Proof that democracy can work at the local level."
- **For staff:** "You are partners, not order-takers."

Same underlying values; different language for different contexts.

**Why this matters:**
If governance is just internal mechanics, no one outside cares. Narrative is how we communicate why this matters and how it serves people.

**Output:** Clear messaging aligned with actual values (not marketing BS)

---

### Phase 5: Co-Creation (Governance Mechanisms)
**File:** `phase-5-cocreation.json`

The library operationalizes community voice with:

**Governance Council:**
- 7 elected community members
- 2 staff representatives (elected by staff)
- Director (hired by Council; reports to Council)

**Decision Types:**
- Budget: Council majority vote
- Contested collection items: Community advisory vote + Council final decision
- Major policies: Council 2/3 majority; 30-day community notice
- Director hire/fire: Council vote (unanimous to fire)

**Participation Mechanisms:**
- Open monthly Council meetings
- Community comment periods (30 days before major decisions)
- Annual Community Assembly
- Specialty advisory committees (youth, seniors, multilingual, etc.)

**Accountability:**
- Annual public governance report
- Community feedback surveys
- Council performance review by community

**Why this matters:**
Narrative without mechanisms is theater. These mechanisms are the hard part: defining exactly how community voice happens, not just saying it matters.

**Output:** Specific governance structure; clear processes; real power distribution

---

### Phase 6: Guardian (Value Preservation)
**File:** `phase-6-guardian.json`

The library installs mechanisms to detect and correct drift from core values:

**Monitoring:**
- **Annual Values Audit:** Are we living our four core values?
- **Refusal Registry:** Have any of our refusals been violated?
- **Community Feedback:** Do people feel heard? Do they trust us?

**Escalation Protocol:**
- Level 1 (minor drift): Document & discuss in Council
- Level 2 (pattern): Audit decisions; report to community
- Level 3 (fundamental violation): Community assembly; possible Council reconstitution

**Long-term Preservation:**
- Written library constitution (reviewed every 5 years)
- Constitutional convention every 10 years
- 2/3 community vote required for amendments

**Why this matters:**
Without Guardian, values drift is nearly inevitable. Good people on a Council gradually make small compromises. In 10 years, the library has drifted. Guardian catches this early and corrects.

**Output:** Self-correcting system; institutional values survive beyond individual leaders

---

## What This Example Teaches

### The six phases create a coherent system:

- **Phase 0-2 (Sense):** Understand the world and ourselves
- **Phase 3-4 (Design):** Decide what we'll protect and how we'll talk about it
- **Phase 5-6 (Act):** Build mechanisms and guard them

### Each artifact is machine-readable JSON

All examples validate against the schemas in `../../schemas/`. You can use them to test your own runtime, schema validation, or governance tools.

### The narrative is honest

This example doesn't pretend democracy is easy or that governance takes no time. It shows:
- Real trade-offs (more inclusive = slower initially)
- Real risks (explicit values create accountability; communities can disagree)
- Real mechanisms (not inspirational BS; actual decision processes)

### Values create accountability

Notice how Phase 6 refers back to Phase 2 (Brand DNA) and Phase 3 (Refusals). The Guardian doesn't ask: "Are we making money?" or "Are we efficient?" It asks: "Are we living our values?"

---

## How to Use This Example

### To understand SPECULA:
Read the phases in order (0 → 1 → 1.5 → 2 → 3 → 4 → 5 → 6). Each one builds on the last.

### To validate your schemas:
```bash
cd ../../../  # back to specula-framework root
python -m specula_agent validate schemas/phase0_activation.schema.json ../examples/basic-case/phase-0-activation.json
# ... repeat for each phase
```

### To build your own governance journey:
Copy this directory. Rename `phase-*.json` files with your project name. Edit payloads to match your context. Use this example as a template.

### To teach others about SPECULA:
Share the `README.md` + all 6 JSON files. It's a complete worked example that shows how abstract principles become concrete governance.

---

## Questions This Example Raises

**For library:** What governance structure makes both "Civic Hub" and "Resilience against Politicization" possible?

**For community:** Do we actually want this much voice in decisions? What are we willing to invest in?

**For society:** Can publicly-governed institutions compete with corporate platforms while maintaining values?

The SPECULA Method doesn't answer these questions. It gives you a process to answer them for your context.

---

**Last updated:** 2026-03-29  
**Status:** Complete example; ready for community governance launch  
**Files:** 7 JSON artifacts + this README
