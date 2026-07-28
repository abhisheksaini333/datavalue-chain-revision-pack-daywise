# Day 2 - Agentic Data Engineering And Pipelines - Learner Revision, Diagrams And Study Pack

Share this Markdown with learners after class. It is written for revision, redraw practice and hands-on follow-up. It does not include private lab credentials, URLs, tokens or screenshots.

## 1. Today In One Paragraph

Today focused on **dbt, orchestration, CDC, self-healing, memory, human approval**. The main idea is to move from tool usage to visible evidence: dataset, business decision, practical proof, risk, control, GCP translation and a saved artifact that another person can review.

**Memory line:** Signal is not diagnosis. A failed row count tells you something changed; it does not tell you what to repair.

## 2. Course Syllabus Outcomes Covered

- Build an ELT pipeline with model, test and run log.
- Explain orchestration with Airflow/Dagster/Prefect style DAG thinking.
- Use AI to draft pipeline code safely, then inspect and correct it.
- Simulate schema drift and write a monitor-diagnose-fix decision log.

## 3. Dataset, Tools And Saved Evidence

| Item | What to remember |
|---|---|
| Demo lane | `Insurance` |
| Primary dataset | `Insurance/Insurance Claims and Policy Data/Insurance Claims and Policy Data.zip` |
| Fallback dataset | `Insurance/Insurance/insurance_cash_application.csv` |
| VM evidence folder | `Persistent_Folder/day-02-evidence` |
| Main Markdown artifact | `day-02-insurance-pipeline-run-log.md` |
| Notebook/proof file | `day-02-bronze-silver-gold-pipeline.ipynb` |
| GCP translation | BigQuery transformation pipeline, Cloud Functions trigger concept, Airflow/Composer concept, Secret Manager for credentials |
| AI assistants | Codex or Claude Code may draft, explain or inspect. Learners must review before accepting. |

## 4. Practical Steps Learners Should Be Able To Repeat

1. Open the insurance claims pipeline artifact and VM notebook.
2. Create bronze, silver and gold proof or a run-summary table.
3. Simulate schema drift and separate signal from diagnosis.
4. Design a Claude-powered monitor that proposes a patch but does not approve it.
5. Map Airflow REST, dbt, schema registry, BigQuery, Secret Manager, MCP/tool runner and vector memory.
6. Save the artifact, write one limitation honestly, and be ready to explain what evidence proves the work.

## 5. Live-Class Flow Recap

| Time | What happened | Revision task |
|---|---|---|
| 11:00-11:10 | Fast Start And Recall | Explain the evidence or decision produced in this segment. |
| 11:10-11:35 | Mini Lecture 1: Simple Concept Before Tool | Write the concept in your own words. |
| 11:35-12:05 | Mini Lecture 2: Course Syllabus Topics In Plain English | Write the concept in your own words. |
| 12:05-12:35 | Practical 1: Create Evidence Trail | Repeat the step or inspect the saved artifact. |
| 12:35-13:05 | Practical 2: Open Dataset And Create Smallest Visible Proof | Repeat the step or inspect the saved artifact. |
| 13:05-13:35 | Practical 3: Use Codex Or Claude Code Safely | Repeat the step or inspect the saved artifact. |
| 13:35-14:20 | Practical 4: Build The Main Day Artifact | Repeat the step or inspect the saved artifact. |
| 14:20-14:45 | Misconceptions And Real-World Example | Explain the evidence or decision produced in this segment. |
| 16:00-16:15 | Restart From Saved Proof And Re-Anchor | Explain the evidence or decision produced in this segment. |
| 16:15-16:35 | Lab 5: Harden The VM Pipeline Proof | Repeat the step or inspect the saved artifact. |
| 16:35-17:05 | GCP Translation Lab A: BigQuery Pipeline Mapping | Repeat the step or inspect the saved artifact. |
| 17:05-17:30 | GCP Translation Lab B: Cloud Functions Trigger Concept | Repeat the step or inspect the saved artifact. |
| 17:30-17:50 | GCP Translation Lab C: Secret Manager And Cloud Composer | Repeat the step or inspect the saved artifact. |
| 17:50-18:10 | Mini Lecture 4: Claude For Data Engineering And Tool Calling | Write the concept in your own words. |
| 18:10-18:35 | Practical 6: Build The H1 Insurance Claude-Powered Pipeline Agent Design | Repeat the step or inspect the saved artifact. |
| 18:35-18:55 | Pipeline Memory, Guardrails, Legacy Compatibility And Coverage Check | Explain the evidence or decision produced in this segment. |
| 18:55-19:15 | Ship Review And Peer Review | Check that the artifact is defensible and complete. |
| 19:15-19:30 | Feedback, Homework And Close | Check that the artifact is defensible and complete. |

## 6. Key Concepts In Simple Words

| Concept | Simple meaning |
|---|---|
| Agentic pipeline | A pipeline with monitor, diagnose, propose, approve, execute and learn steps around it. |
| Signal versus diagnosis | A signal says something may be wrong; diagnosis explains why using evidence. |
| Claude for data engineering | Claude Code can draft code; Claude apps can diagnose from structured evidence; tool calling lets an app execute controlled functions. |
| Keep model out of data path | Raw data stays in the platform; the model receives small evidence and proposes changes. |
| Pipeline memory | A vector/searchable store of failures, fixes, decisions and evidence for future incidents. |
| Guardrails for autonomy | Read-only by default, approvals for risky writes, decision logs, idempotent and reversible operations. |
| Legacy compatibility | Agents should wrap existing Airflow DAGs, Spark jobs and dbt models without forcing a rebuild. |
| Artifact | A saved proof file that another person can inspect later. |
| Evidence | A visible output such as a query result, row count, test result, log, screenshot note, or reviewed markdown. |
| Control before trust | A check, approval, policy or audit record that must exist before a data or AI output is trusted. |
| Trust boundary | The line between what an AI/tool may suggest and what a human or governed platform may approve or execute. |
| GCP translation | The cloud-managed equivalent of what was first proved in the VM sandbox. |

## 7. Diagrams To Redraw And Revise

Redraw these diagrams by hand or in Mermaid. For each arrow, say what responsibility moves from one box to the next and what evidence proves the step.

### Diagram 1: Agentic Pipeline Loop

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    Source[Claims source] --> Bronze[Bronze load]
    Bronze --> Silver[Clean transform]
    Silver --> Gold[Gold table]
    Gold --> Test[Tests]
    Test -->|pass| Publish[Publish]
    Test -->|fail| Monitor[Monitor]
    Monitor --> Diagnose[Diagnose]
    Diagnose --> Approve[Human approval]
    Approve --> Fix[Fix and rerun]
```

### Diagram 2: Signal Versus Diagnosis

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart TD
    Alert[Failed test] --> Signal[Signal]
    Signal --> Evidence[Schema logs counts]
    Evidence --> Cause[Root cause]
    Cause --> Repair[Repair proposal]
    Repair --> Approval[Approval gate]
    Approval --> Rerun[Rerun proof]
```

### Diagram 3: Keep Model Out Of Data Path

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    AI[AI drafts code] --> Review[Human review]
    Review --> Tool[dbt or Python executes]
    Tool --> Result[Small result]
    Result --> Log[Decision log]
    AI -. no direct write .-> Block[Production data]
```

### Diagram 4: Pipeline Memory

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart TD
    Incident[Incident] --> Fix[Fix]
    Fix --> Decision[Decision]
    Decision --> Memory[Vector incident memory]
    Memory --> Future[Future diagnosis]
```

### Diagram 5: Evidence Loop Used Every Day

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    Concept[Concept] --> Demo[Instructor demo]
    Demo --> Learner[Learner practical]
    Learner --> Output[Visible output]
    Output --> Artifact[Saved artifact]
    Artifact --> Review[Peer or instructor review]
    Review --> Improve[Improve proof]
```

### Diagram 6: VM To GCP Translation Map

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    VM[VM sandbox proof] --> Folder[Persistent_Folder evidence]
    Folder --> Concept[Concept proven locally]
    Concept --> GCP[GCP managed service]
    GCP --> Control[IAM secrets audit cost]
    Control --> Note[Write translation in artifact]
```

### Diagram 7: 16:00-16:15 - Restart From Saved Proof And Re-Anchor

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    A[Saved VM evidence] --> B[Harden pipeline proof]
    B --> C[Translate to BigQuery]
    C --> D[Translate triggers to Cloud Functions]
    D --> E[Protect secrets with Secret Manager]
    E --> F[Map orchestration to Composer or Airflow]
    F --> G[Document controls and ship]
```

### Diagram 8: 7. Second-Half VM Proof Hardening

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart TD
    Raw[Bronze: raw claims data] --> Clean[Silver: cleaned claims data]
    Clean --> Gold[Gold: decision-ready claims summary]
    Gold --> Monitor[Monitor: check output quality]
    Monitor --> Signal{Signal found?}
    Signal -- No --> Save[Save successful evidence]
    Signal -- Yes --> Diagnose[Diagnose root cause]
    Diagnose --> Propose[Propose fix]
    Propose --> Approve{Human approves?}
    Approve -- No --> Log[Log rejection and reason]
    Approve -- Yes --> Rerun[Rerun controlled step]
    Rerun --> Save
```

### Diagram 9: 8.1 BigQuery Mapping

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    VMFile[VM file: insurance claims] --> BQBronze[BigQuery claims_bronze]
    BQBronze --> BQSilver[SQL transform: claims_silver]
    BQSilver --> BQGold[SQL transform: claims_gold_summary]
    BQGold --> Quality[Validation SQL]
    Quality --> Evidence[Saved evidence: row count, pass/fail, job note]
    Evidence --> Decision[Business decision]
```

### Diagram 10: 8.2 Cloud Functions Trigger Mapping

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
sequenceDiagram
    participant File as Claims file/event
    participant Fn as Cloud Function
    participant BQ as BigQuery
    participant Log as Run log
    participant Human as Human approver
    File->>Fn: New file or event arrives
    Fn->>Fn: Check name, size, metadata
    Fn->>Log: Record trigger evidence
    Fn->>BQ: Start/load/check table when valid
    Fn->>Human: Ask for approval if risky repair is needed
    Human-->>Fn: Approve or reject
```

### Diagram 11: 8.4 Composer / Airflow Orchestration Mapping

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart TD
    subgraph SecretBoundary[Secret boundary]
        SM[Secret Manager: stores secret value]
        IAM[IAM: controls who can read]
    end
    Code[Pipeline code or function] -->|requests secret by name| SM
    IAM -->|allows or denies| SM
    SM -->|returns value only to allowed runtime| Code
    Code --> BQ[BigQuery job]
```

### Diagram 12: 8.4 Composer / Airflow Orchestration Mapping

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    Start[DAG start] --> Load[Load bronze claims]
    Load --> Clean[Clean silver claims]
    Clean --> Test[Run quality checks]
    Test --> Gate{Risky fix needed?}
    Gate -- No --> Publish[Publish gold output]
    Gate -- Yes --> Approval[Human approval task]
    Approval --> Publish
    Publish --> Notify[Notify and save evidence]
```

### Diagram 13: 9.1 Claude Usage Modes

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    Evidence[Small pipeline evidence] --> Claude[Claude diagnosis and patch proposal]
    Claude --> ToolCall[Structured tool/function call request]
    ToolCall --> App[Application or MCP tool runner]
    App --> Platform[Airflow, dbt, BigQuery, schema registry]
    Platform --> Result[Small execution result]
    Result --> Claude
    Result --> Log[Decision and evidence log]
```

### Diagram 14: 10.2 Sample Claude Diagnosis

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart TD
    Airflow[Airflow REST API: DAG status] --> Agent[Claude pipeline monitor]
    DBT[dbt run/test result] --> Agent
    Schema[Schema diff] --> Agent
    Agent --> Diagnosis[Diagnosis]
    Agent --> Patch[Proposed SQL/dbt patch]
    Patch --> Approval{Human approval}
    Approval -- Reject --> LogReject[Record rejection]
    Approval -- Approve --> Runner[Separate tool runner]
    Runner --> DBTRun[Trigger dbt/Airflow run]
    DBTRun --> BQ[Validate in BigQuery]
    BQ --> Memory[Write pipeline memory]
```

### Diagram 15: 10.2 Sample Claude Diagnosis

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
sequenceDiagram
    participant Monitor as Monitor agent
    participant Airflow as Airflow REST API
    participant dbt as dbt job/test API
    participant Schema as Schema registry
    participant Human as Human approver
    participant Runner as Tool runner
    Monitor->>Airflow: get latest failed DAG run
    Airflow-->>Monitor: failed task and log summary
    Monitor->>dbt: get failed test/model details
    dbt-->>Monitor: failed model and error
    Monitor->>Schema: get schema diff
    Schema-->>Monitor: claim_amount changed to amount_claimed
    Monitor->>Human: propose patch and request approval
    Human-->>Runner: approve or reject
    Runner->>Airflow: trigger DAG only after approval
```

### Diagram 16: 12. Day 2 Course Syllabus Coverage Check

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    Raw[Raw data path] --> Platform[BigQuery, Spark, dbt, Airflow]
    Platform --> Output[Trusted output]
    Platform --> SmallEvidence[Small evidence: status, schema diff, failed test]
    SmallEvidence --> Model[Claude]
    Model --> Draft[Diagnosis and patch draft]
    Draft --> Approval{Approval gate}
    Approval -- Approved --> ToolRunner[Tool runner executes]
    Approval -- Rejected --> DecisionLog[Decision log]
    ToolRunner --> Platform
```

### Diagram 17: 12. Day 2 Course Syllabus Coverage Check

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart TD
    Incident[New pipeline failure] --> Retrieve[Retrieve similar memories from vector store]
    Retrieve --> Compare[Compare old fix with current evidence]
    Compare --> Draft[Draft diagnosis and patch]
    Draft --> Approval[Human approval]
    Approval --> Save[Save new incident memory]
    Save --> Future[Future incidents become easier]
```

### Diagram 18: 12. Day 2 Course Syllabus Coverage Check

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    ExistingAirflow[Existing Airflow DAG] --> AgentLayer[Agent layer]
    ExistingSpark[Existing Spark job] --> AgentLayer
    ExistingDbt[Existing dbt project] --> AgentLayer
    ExistingSchema[Existing schema registry] --> AgentLayer
    AgentLayer --> Monitor[Monitor]
    AgentLayer --> Diagnose[Diagnose]
    AgentLayer --> Propose[Propose]
    AgentLayer --> Approve[Request approval]
```

### Diagram 19: 16. Failure Injection And Recovery Scenario

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart TD
    NewFile[New claims file arrives] --> Check[Validation check]
    Check --> Fail{Expected column present?}
    Fail -- Yes --> Continue[Continue pipeline]
    Fail -- No --> Signal[Signal: missing claim_amount]
    Signal --> Diagnose[Diagnose: source column changed]
    Diagnose --> Propose[Propose mapping amount_claimed -> claim_amount]
    Propose --> Approval{Human approval}
    Approval -- Reject --> Stop[Stop and document]
    Approval -- Approve --> Update[Update mapping]
    Update --> Rerun[Rerun silver and validation]
    Rerun --> Publish[Publish gold output]
    Publish --> Evidence[Save evidence]
```

### Diagram 20: 18. Peer Review

Revision prompt: explain each box, then name one risk and one control for this flow.

```mermaid
flowchart LR
    Monitor[Monitor agent] --> Signal[Signal]
    Signal --> Diagnose[Diagnosis agent]
    Diagnose --> Proposal[Repair proposal]
    Proposal --> Human[Human approval]
    Human --> Execute[Controlled execution]
    Execute --> Memory[Pipeline memory]
    Memory --> Monitor
```

## 8. Revision Notes And Checks

- Do not say a tool was used unless you can point to evidence.
- Do not trust AI output until the source, permission, test result or approval is visible.
- Do not include secrets, tokens, private URLs or credentials in shared artifacts.
- For every practical, be able to answer: what data, what output, what risk, what control, what limitation?
- For every GCP translation, be able to say what the VM proved and what the managed service would own in production.

## 9. Self-Quiz

| # | Question | Expected answer shape |
|---:|---|---|
| 1 | What is the main artifact for today? | Name the exact `.md` file and evidence folder. |
| 2 | What business decision does the artifact support? | Say the decision and why wrong data would hurt it. |
| 3 | What is the strongest proof you saved? | Name a row count, output, diagram, test, log, decision or review. |
| 4 | What is the main trust boundary? | Say what AI/tool may suggest and what needs platform or human control. |
| 5 | What is the GCP translation? | Name the GCP services and their responsibility. |

## 10. Practice Before The Next Class

Spend 20-30 minutes improving the saved artifact:

1. Add one stronger proof line.
2. Add or redraw one Mermaid diagram from this pack.
3. Add one clearer risk and one control before trust.
4. Add one honest limitation: what the class demo does not prove yet.
5. Add one question to bring to the next class.

## 11. Shareable Checklist

- [ ] My artifact is saved in the persistent folder.
- [ ] My artifact names the dataset or fallback dataset.
- [ ] My artifact includes the business decision.
- [ ] My artifact includes at least one visible proof.
- [ ] My artifact includes at least one risk and one control.
- [ ] My artifact includes the GCP translation.
- [ ] My artifact does not expose secrets or private lab access.
- [ ] I can explain at least two diagrams without reading the full script.

## 12. Further Study Links

Use these for follow-up reading. Prefer official documentation when tool behavior matters.

- [Airflow DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- [Airflow Tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html)
- [Airflow architecture overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
- [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)
- [dbt Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl)
- [dbt semantic models](https://docs.getdbt.com/docs/build/semantic-models)
- [BigQuery quickstart: load and query data in the console](https://docs.cloud.google.com/bigquery/docs/quickstarts/load-data-console)
- [Run BigQuery queries](https://docs.cloud.google.com/bigquery/docs/running-queries)
- [BigQuery partitioned tables](https://docs.cloud.google.com/bigquery/docs/partitioned-tables)
- [BigQuery clustering](https://docs.cloud.google.com/bigquery/docs/clustering-overview)
- [BigQuery time travel and historical data](https://docs.cloud.google.com/bigquery/docs/time-travel)
- [Cloud Storage buckets](https://docs.cloud.google.com/storage/docs/creating-buckets)
- [Secret Manager overview](https://docs.cloud.google.com/secret-manager/docs/overview)
- [Cloud Run deploy from source](https://docs.cloud.google.com/run/docs/deploying-source-code)
- [Cloud Functions concepts](https://docs.cloud.google.com/functions/docs/concepts/overview)
- [Firestore overview](https://docs.cloud.google.com/firestore/docs/overview)
- [Pub/Sub overview](https://docs.cloud.google.com/pubsub/docs/overview)
- [Apache Airflow DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- [Apache Airflow REST API](https://airflow.apache.org/docs/apache-airflow/2.10.4/stable-rest-api-ref.html)
- [BigQuery documentation](https://docs.cloud.google.com/bigquery/docs)
- [Vertex AI RAG Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview)
- [Model Context Protocol tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

## 13. Bridge To The Next Day

Tomorrow should not restart from zero. Bring forward today's saved artifact, strongest proof, weakest risk/control, and one question. The next class builds on this evidence.
