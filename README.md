# InspectR

_**Thesis Title:** Architecting a Policy Engine for AI/data Operations and Pipeline Ecosystems using a Policy-as-Code (PaC) Framework._

> InspectR is a design‑time policy engine that operationalises regulatory requirements (GDPR / AIA) as Policy‑as‑Code, by utilising decoupled OPA/Rego rules to statically assess pipeline blueprints and outputs machine‑readable governance results pre‑deployment.

> InspectR investigates the boundaries of compliance automation and how regulatory requirements can be operationalised into traceable, evidence-bound, machine-checkable design-time policies.

## 1. Research Profile
| | |
| :--- | :--- |
| **Research Frontier** | Compliance automation - translating legal documents into deterministic software logic |
| **Research Methodology** | Design Science Research (**DSR**): designing and building a technical artefact to solve a real-world problem. **Research – Build – Evaluate**. |
| **Research Artefact** | **InspectR** — A standalone design-time policy validation engine. |
| **Core Disciplines** | Systems Architecture & Engineering, Compliance Engineering, Policy-as-Code (PaC). |
| **Application Domain** | AI/Data Operations, compliance-aware data pipelines, and heterogeneous architectures. |
| **Architectural Context** | Policy-as-Code, Open Policy Agent (OPA), LLM-generated data pipeline structures and multi-agent workflows (e.g., policy interpreter agents, remedy generator agents). |
| **Technical Stack** | Python, Plotly, Pandas, JSON, Policy-as-Code, Open Policy Agent (OPA), Rego, inLUMEN, Streamlit |
| **Industrial Context** | SINTEF Digital, DataPACT  |
| **Legal Domain** | 1️⃣ Privacy and GDPR with Use Case #1: MUNDAT, 2️⃣ EU AI Act (AIA) with Use Case #2 |

---

**Core definitions**

- **Law** is the mandatory requirement set by governments (e.g., GDPR, EU AI Act) that carries legal penalties for non-compliance.
- **Policy** is the internal interpretation of the law by an organisation, translating those external laws into specific, actionable workplace rules.
- **Compliance** is the ongoing execution and proof that the organisation is actually following both the internal policies and external laws.


# USE CASE: MUNDAT (TK UC) 
This PoC uses the **MUNDAT: Trondheim Kommune (TK) use case** and selected provisions of the **GDPR** to demonstrate the approach.The PoC evaluates a static **inLUMEN TK pipeline blueprint** directly against independently defined **Rego policies** using **Open Policy Agent (OPA)**.

This document outlines the three validation scenarios used to test the **InspectR** policy engine. It demonstrates how a generic **7-stage *inLUMEN* pipeline design** maps directly to the datasets, user stories, and requirements of the **Trondheim MUNDAT** use case.

---

## 1. TK Test Case 1: The "PASS" Scenario 

### MUNDAT Context Mapping
*   **Dataset:** `IoT` Stormwater Basin Sensors (Time-series data, size ~50 MB, contains no personal data, under an Open License).
*   **User Story:** **TK.US.09 / TK.US.10** (Data Consumer accessing pre-authorized, open datasets to provide automated services efficiently).
*   **Functional Requirement:** **TK.FR.01** (Dataset uses a standardized metadata vocabulary to prove its public nature).

### 7-Stage Pipeline Configuration
1.  **Stage 1 (Ingest):** Connected to the `IoT_Stormwater_Basin_Sensors` source.
2.  **Stage 2 (Triage):** `classification` set to `public_environmental`.
3.  **Stage 3 (Pre-Processing):** Core data cleaning and timestamp harmonization.
4.  **Stage 4 (Risk Assessment):** System flags `dpia_required` as `false` since it lacks PII.
5.  **Stage 5 (Transformation):** `action` is set to `none` (No structural data protection needed).
6.  **Stage 6 (Access Control):** Protocols default to public `open_access`.
7.  **Stage 7 (Egress):** Pipeline targets the `Open_Data_Portal`.

### InspectR Output Performance
*   **Status:** ✅ **PASS**
*   **Explanation:** Design-time structural validation successful. Safe pathing confirmed for non-personal environmental metrics routing directly to a public endpoint.
*   **Exact Evidence:** `input.data_type == "Non-Personal"` maps smoothly to `input.stages.target == "Open_Data_Portal"`.
*   **Remedy Suggestion:** None required. The design meets all automated constraints and is safe for compilation in *inLUMEN*.

---

## 2. TK Test Case 2: The "FAIL" Scenario (Critical PII Exposure)

### MUNDAT Context Mapping
*   **Dataset:** `Sickleave` HR Dataset (Aggregated demographic and monthly rotation survey records containing indirect PII).
*   **User Story:** **TK.US.01 / TK.US.12** (Compliance Process Owner evaluating data requests and requiring automated support to detect indirect identification risks).
*   **Functional Requirement:** **TK.FR.03 / TK.FR.10** (System must automatically identify compliance defects and tag unprotected PII from a data flow configuration).

### 7-Stage Pipeline Configuration
1.  **Stage 1 (Ingest):** Connected to `HR_System_Job_Rotation_Units`.
2.  **Stage 2 (Triage):** `classification` set to `sensitive_hr_metrics`.
3.  **Stage 3 (Pre-Processing):** Pipeline runs standard internal harmonization.
4.  **Stage 4 (Risk Assessment):** System sets `dpia_required` to `true` due to sensitive content.
5.  **Stage 5 (Transformation):** **CRITICAL FLAW:** `action` is set to `passthrough` (Missing anonymization).
6.  **Stage 6 (Access Control):** Architecture leaves paths `unencrypted`.
7.  **Stage 7 (Egress):** Pipeline erroneously targets the public-facing `Open_Data_Portal`.

### InspectR Output Performance
*   **Status:** ❌ **FAIL**
*   **Explanation:** CRITICAL COMPLIANCE FAILURE: Personally Identifiable Information (PII) from municipal databases cannot be exposed to a public target without active transformation layers.
*   **Exact Evidence:** `input.data_type == "Personal_Data"` routing to `Open_Data_Portal` while Stage 5 protection count equals 0.
*   **Remedy Suggestion:** 
    *   *Human-Readable:* "Insert an active anonymization or pseudonymization block at Stage 5 before routing data to a public egress portal."
    *   *Machine-Readable:* `{"action": "modify_node", "target_stage": 5, "required_properties": {"action": "anonymisation"}}`

---

## 3. TK Test Case 3: The "HUMAN" Scenario (Conditional Data Governance Triage)

### MUNDAT Context Mapping
*   **Dataset:** `Sickleave` HR Dataset (Requested by academic research teams for algorithmic data innovation).
*   **User Story:** **TK.US.03 / TK.US.04 / TK.US.11** (Compliance Process Owner managing data-sharing contracts and verifying legal/ethical boundaries before formal delivery).
*   **Functional Requirement:** **TK.FR.04 / TK.FR.14** (System must flag conditional issues requiring complex contract evaluation or high-level management verification).

### 7-Stage Pipeline Configuration
1.  **Stage 1 (Ingest):** Connected to `HR_System_Age_Distribution`.
2.  **Stage 2 (Triage):** `classification` set to `academic_request`.
3.  **Stage 3 (Pre-Processing):** Running data cleaning and structural interpretation.
4.  **Stage 4 (Risk Assessment):** Flagged for mandatory review (`dpia_required: true`).
5.  **Stage 5 (Transformation):** `action` is properly set to `anonymisation`.
6.  **Stage 6 (Access Control):** Secured via `token_restricted` architecture.
7.  **Stage 7 (Egress):** Pipeline targets a restricted `Secure_Controlled_Vault`.
8.  **Metadata Defect:** The crucial field `contract_verified` is toggled to `false`.

### InspectR Output Performance
*   **Status:** ⚠️ **HUMAN**
*   **Explanation:** CONDITIONAL HOLD: The structural architecture of the data pipeline handles masking and encryption rules correctly, but missing legal clearance tokens prevent automated authorization.
*   **Exact Evidence:** `input.data_type == "Personal_Data"` with active masking routing to a protected vault, but metadata token validation fails (`input.metadata.contract_verified == false`).
*   **Remedy Suggestion:** 
    *   *Human-Readable:* "Triage this design to the Compliance Process Owner and Data Protection Officer to verify the physical data-sharing contract and apply the approved contract token."
    *   *Machine-Readable:* `{"action": "triage_to_governance", "required_roles": ["Compliance_Process_Owner", "Data_Protection_Officer"]}`


### Components

1. **Pipeline blueprint = EVIDENCE**

   The inLUMEN JSON contains the design-time facts InspectR can inspect.

2. **Organisational policy = CONDITION / REQUIREMENT**

   It defines what evidence is expected and what should count as acceptable, unacceptable, or insufficient.

3. **Rego = EXECUTABLE REPRESENTATION OF THAT POLICY**

   The organisational policy conditions are encoded as machine-executable Rego rules.

4. **OPA = EVALUATOR**

   OPA takes:

   ```text
   Pipeline blueprint (evidence)
           +
   Rego rules (encoded policy)
           ↓
        evaluates
           ↓
   OK / FAIL / HUMAN
   ```

![Architecture diagram](https://github.com/user-attachments/assets/b5a0fdb4-8da4-4e42-b50c-b0fb126dc812)
![Architecture diagram](https://github.com/user-attachments/assets/f8edb06e-723b-495f-ab9b-33f7d579591d)


### Repository Structure

```text
inspectr-poc/
├── app.py          # Application entry point
├── data/           # Pipeline blueprints, datasets and supporting files
├── pages/          # InspectR interface and subpages, taxonomy
├── policies/       # Rego Policy-as-Code rules
├── src/            # Evaluation/integration logic
├── images/         # UI and project assets
└── requirements.txt
```

### Scientific contribution
InspectR demonstrates an architecture and operational method for translating organisational policies into explainable Policy-as-Code controls over static data-pipeline blueprints.

The contribution can be evaluated through:

- separation of policy from application logic;
- independent OPA/Rego decision evaluation;
- explicit evidence requirements;
- traceability from requirement to executable rule;
- distinction between OK, FAIL, and HUMAN;
- conservative treatment of missing or ambiguous evidence;
- applicability to pipeline design before execution;
- use of a realistic municipal data-sharing case.

### Disclaimer
This is a research prototype. InspectR does not certify compliance, determine legal compliance as a whole, encode legal text directly, replace legal interpretation, or execute the pipeline. Results are correct only relative to the explicitly encoded operational policy and available blueprint evidence.

InspectR is an independent, standalone, generic policy engine. This repository showcases only a specific use case (TK use case). The PoC is designed to demonstrate the feasibility of the approach without the complexity of a full implementation. During this PoC implementation of InspectR WE WILL NOT USE IR (the graph model, the Intermediate Representation) for KISS purposes.

InspectR is developed as part of an MSc thesis at the University of Oslo in collaboration with SINTEF and the EU-funded DataPACT project.

> _Research prototype — work in progress_

---

sirin-koca
