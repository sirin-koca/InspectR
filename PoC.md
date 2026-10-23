# InspectR 
### Current version: Proof-of-Concept (PoC)

## Work-in-progress

> InspectR demonstrates an architecture and operational method for translating organisational policies into explainable Policy-as-Code controls over static data-pipeline blueprints.

The contribution can be evaluated through:

- separation of policy from application logic;
- independent OPA/Rego decision evaluation;
- explicit evidence requirements;
- traceability from requirement to executable rule;
- distinction between `OK`, `FAIL`, and `HUMAN`;
- conservative treatment of missing or ambiguous evidence;
- applicability to pipeline design before execution;
- use of a realistic municipal data-sharing case.

## Meaning of “Correct”
The architecture is correct for the PoC if it demonstrates that:

- InspectR does not hard-code compliance decisions in Python;
- Rego contains the executable policy;
- OPA evaluates policy independently;
- the blueprint provides the evidence;
- the application orchestrates and explains results;
- policy results include reasons, evidence, legal or governance references, and remedies;
- missing evidence is distinguishable from explicit non-compliance;
- the scope of each rule is documented.
“Correct” does not mean that a result proves legal compliance. It means that the result is correct relative to the explicitly declared operational rule.

## Meaning of “Novel”
The project does not claim that Policy-as-Code or OPA itself is novel.

The possible contribution is the combination of:

- architectural mechanism that decouples policy and application logic
- compliance inspection at pipeline design time;
- static blueprint evidence;
- regulatory operationalisation;
- explainable Policy-as-Code findings;
- evidence sufficiency handling;
- `PASS / FAIL / HUMAN` decision semantics;
- separation of concerns: policy engine, requirements encoding and pipeline representation.

NB: 
1. The thesis still needs a literature and related-work review to establish whether this combination is genuinely novel.

2. Defining formal rule specification for each policy:
Rule ID
Requirement source
Operational interpretation
Applicability
Required evidence
Blueprint field
Rego condition
PASS meaning
FAIL meaning
HUMAN meaning
Known limitations


## Agreed Boundary

InspectR is an independent, standalone, generic policy engine. 
This repository showcases only a specific use case (TK use case). 
The PoC is designed to demonstrate the feasibility of the approach without the complexity of a full implementation.
PoC implementation excludes IR (the graph model, the Intermediate Representation) for simplicity.

### InspectR PoC definition:
InspectR is a proof-of-concept architecture for design-time AI and data-pipeline compliance tooling. It investigates how the semantic gap between complex regulatory requirements and deterministic software logic can be addressed through Policy-as-Code, using a static TK/MUNDAT pipeline blueprint as the concrete evaluation case. The PoC deliberately omits an Intermediate Representation and evaluates the blueprint directly with OPA/Rego.

---


