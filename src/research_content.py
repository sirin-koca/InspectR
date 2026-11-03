"""Research positioning: key works, gaps, questions, candidate contributions.

Single source for the Research page. Every key work has a verified link.
Candidate contributions are hypotheses to be tested, not claims.
"""

# ---------------------------------------------------------------- key works
# (id, short citation, url, what it offers, stated limitation / future work, relevance)
KEY_WORKS = [
    ("W1", "Hashmi et al., 2018 (KAIS)",
     "https://link.springer.com/article/10.1007/s10115-017-1142-1",
     "Survey of 79 business-process compliance papers: design-time (28%), run-time (32%) and auditing (10%) approaches.",
     "Identifies open research challenges in compliance management.",
     "Positions InspectR as a design-time compliance approach."),
    ("W2", "Torre et al., 2021 (SoSyM)",
     "https://link.springer.com/article/10.1007/s10270-021-00935-5",
     "GDPR as a UML model with 35 compliance rules in OCL; generic and specialised tiers.",
     "Building the instance model from system descriptions is “a prerequisite for automated compliance checking” "
     "([preprint](https://arxiv.org/pdf/2007.12046)); legal validation and traceability are lessons learned.",
     "Closest model-based predecessor. InspectR uses pipeline blueprints instead of UML, and Rego instead of OCL."),
    ("W3", "Pandit et al., 2019 (SEMANTiCS)",
     "https://link.springer.com/chapter/10.1007/978-3-030-33220-4_2",
     "Test-driven, ex-ante GDPR compliance checking over semantically documented processes.",
     "Demonstrated on consent requirements only; a universal ontology “may not be feasible”; "
     "proposes taxonomies and compliance design patterns.",
     "Same test-before-deploy idea; InspectR applies it to pipeline designs."),
    ("W4", "Pandit et al., 2024 (ISWC), DPV 2.0",
     "https://link.springer.com/chapter/10.1007/978-3-031-77847-6_10",
     "W3C vocabulary for machine-readable descriptions of personal-data processing, including GDPR concepts.",
     "A vocabulary, not a checking method.",
     "Candidate vocabulary for the evidence model (RQ1); DataPACT maintains an ODRL-DPV ontology."),
    ("W5", "Vanezi et al., 2026 (SLR, arXiv)",
     "https://arxiv.org/html/2604.16361",
     "Systematic review of modelling GDPR requirements with software-engineering diagrams.",
     "Calls for lifecycle traceability, “tools to support automated compliance checking”, and action-aware "
     "modelling of purpose limitation “beyond simple textual labelling”.",
     "Most recent statement of the tool-support and purpose-limitation gaps."),
    ("W6", "Nogueira & Resende, 2026 (Computers)",
     "https://www.mdpi.com/2073-431X/15/7/453",
     "Reuse of OPA/Rego policies across CI/CD and Kubernetes admission control.",
     "Policies do not cover “regulatory, or domain-specific governance requirements”; expected outcomes were set "
     "by the same authors (experimenter bias).",
     "State of Policy-as-Code: infrastructure, not regulatory obligations on data-pipeline designs."),
    ("W7", "Roman et al., 2022 (IEEE Computer)",
     "https://doi.org/10.1109/MC.2022.3154148",
     "Big-data pipeline lifecycle on the computing continuum (DataCloud). The "
     "[project](https://www.sintef.no/en/projects/2021/datacloud/) “separates the design from the run-time aspects” "
     "of pipelines.",
     "Not assessed here (context work).",
     "Origin of the design-time pipeline models that InspectR inspects."),
    ("W8", "LexAlign, SINTEF (DataPACT)",
     "https://www.sintef.no/en/software/lexalign/",
     "Compliance workspace: regulations as executable decision flows; assesses evidence from SIM-PIPE pipeline dry runs.",
     "Proving that derived obligations are fulfilled “relies on manually gathering evidence” "
     "([SINTEF](https://www.sintef.no/en/digital/master-students/agent-based-controls-for-verifying-regulatory-compliance/)).",
     "Complementary: LexAlign derives which obligations apply; InspectR checks whether the design declares the controls."),
]

METHOD_REFERENCE = ("Hevner et al., 2004 (MISQ)", "https://aisel.aisnet.org/misq/vol28/iss1/6/")

# ---------------------------------------------------------------- gaps
# (id, gap, supported by, addressed by)
GAPS = [
    ("G1", "Automated, tool-supported design-time compliance checking is still lacking.", "W2, W5", "Main RQ, RQ2"),
    ("G2", "The facts a check needs are missing from system and pipeline descriptions and are gathered by hand.", "W2, W8", "RQ1"),
    ("G3", "Policy-as-Code targets infrastructure configurations, not regulatory obligations on data-pipeline designs.", "W6", "RQ2"),
    ("G4", "Traceability between requirement, design and verdict is weak.", "W2, W5", "RQ2, RQ3"),
    ("G5", "Purpose limitation and similar judgements resist structural checking.", "W5, W3", "RQ1, RQ2"),
    ("G6", "Rule fidelity needs legal validation; author-defined expected outcomes bias evaluation.", "W2, W6", "RQ3"),
    ("G7", "Result semantics for missing evidence: v1 rules gave false PASS (iteration 1, defects D1–D4).",
     "Own observation; not yet located as a stated gap", "RQ2"),
]

# ---------------------------------------------------------------- research questions
MAIN_RQ = (
    "How can a design-time policy engine be architected to inspect compliance properties of data/AI "
    "pipeline blueprints in a way that is traceable, reliable and independent of the use case and pipeline tool?"
)

# (rq, title, question)
RQS = [
    ("RQ1", "Evidence model",
     "What compliance-relevant information must a pipeline blueprint contain for policy-based inspection? How much "
     "of it can be derived from pipeline tooling (inLUMEN exports and run records), and how much needs manual annotation?"),
    ("RQ2", "Architecture",
     "Which architectural design supports reuse across use cases and blueprint formats: an intermediate "
     "representation with tool adapters, interchangeable policy packs, explicit result semantics for missing information?"),
    ("RQ3", "Evaluation",
     "How reliable, explainable and efficient are InspectR's findings compared with a manual expert review, "
     "across three DataPACT use cases?"),
]

# (rq, candidate sub-question, gap)
SUB_QUESTIONS = [
    ("RQ1", "Which facts do the rules of each use case need (fact inventory)?", "G2"),
    ("RQ1", "Which facts are structural, derivable, manual or human judgement (S / D / M / H)?", "G2, G5"),
    ("RQ1", "Can an existing vocabulary (DPV) represent these facts?", "G2"),
    ("RQ2", "What intermediate representation lets adapters for different tools feed the same rules?", "G1, G3"),
    ("RQ2", "Can policy packs for new use cases be added without changing engine code?", "G3"),
    ("RQ2", "Which result semantics prevent false PASS under missing evidence?", "G7"),
    ("RQ3", "How far do InspectR's findings agree with expert review on seeded defects?", "G6"),
    ("RQ3", "Do stakeholders understand the findings and their limits?", "G4"),
    ("RQ3", "What effort do metadata preparation and review take, compared with manual review?", "G1"),
]

# ---------------------------------------------------------------- candidate contributions
# (id, candidate contribution, type, gap, rq, evidence so far)
CONTRIBUTIONS = [
    ("C1", "Evidence model for compliance-inspectable pipeline blueprints, with fact provenance classes and a measured "
           "tooling gap (native export vs. enriched blueprint).",
     "Design knowledge", "G2, G5", "RQ1", "TK fact inventory; raw export vs. enriched blueprint"),
    ("C2", "Reference architecture: intermediate representation, tool adapters, policy packs and a uniform result contract.",
     "Artefact", "G1, G3", "RQ2", "Result contract and per-rule evaluation; intermediate representation and adapters not yet built"),
    ("C3", "Result semantics for design-time inspection under incomplete evidence (six statuses, fail-safe default).",
     "Design knowledge", "G7, G5", "RQ2", "Status model; D1–D4 removed; 21/21 scenario results as expected"),
    ("C4", "Traceable rule pattern: requirement → IF trigger THEN control → decision table → tests.",
     "Method", "G4, G6", "RQ2, RQ3", "TK-R1–R3; 29 Rego and 20 integration tests"),
    ("C5", "Evaluation of design-time inspection against expert review across use cases, with seeded defects and an ablation.",
     "Empirical", "G6, G1", "RQ3", "Planned (baselines B1, B2)"),
    ("C6", "Positioning of deterministic design-time inspection next to obligation derivation (LexAlign) in a "
           "compliance-by-design toolchain.",
     "Design knowledge", "G2", "Main RQ", "Conceptual; to be agreed with SINTEF"),
]

# ---------------------------------------------------------------- evaluation
# (metric, answers, baseline)
EVALUATION = [
    ("Precision, recall and F1 on seeded defects", "RQ3 · reliability", "B1 expert review"),
    ("False-PASS rate when information is missing", "RQ2, RQ3 · semantic soundness", "B2 ablation (v1 semantics)"),
    ("Agreement with experts (Cohen's kappa)", "RQ3 · fidelity", "B1"),
    ("Evidence coverage: facts derived natively vs. annotated", "RQ1", "Native export"),
    ("Portability: policies reused, adapted or new; adapter effort", "RQ2", "Per use case"),
    ("Effort: metadata preparation and review time", "RQ3 · efficiency", "B1"),
    ("Explainability questionnaire", "RQ3", "Stakeholders"),
]

# ---------------------------------------------------------------- directions
# (direction, gap, source)
DIRECTIONS = [
    ("Derive facts from tool exports and run records (inLUMEN, SIM-PIPE) instead of manual annotation.", "G2", "W2, W8"),
    ("Map blueprint facts to DPV for interoperability with DataPACT policy tools.", "G2", "W4"),
    ("Path- and order-aware rules (e.g. checkpoint before transfer).", "G5", "W5"),
    ("Re-inspection on every design change (CI-style gate for pipeline designs).", "G1, G3", "W6"),
    ("Hand obligations from LexAlign to InspectR as rule triggers.", "G2", "W8"),
    ("Independent expert validation of rule fidelity.", "G6", "W2, W6"),
]
