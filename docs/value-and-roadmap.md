# Project value, positioning, and roadmap

This document explains why `evidence-workflows` could become a valuable open-source project, what it is worth today, and what must be built before making larger claims.

## 1. The thesis in one sentence

`evidence-workflows` can become an open contract layer that converts an implicit human/team standard into a public policy, guides someone to complete an evidence-bearing artifact, evaluates it deterministically, and hands a safe result to operational systems.

That is a larger opportunity than “AI-generated worklogs,” but only if the project earns trust and becomes interoperable.

## 2. Honest assessment of the current release

The current `0.1.0` release has real but narrow value:

- A team can turn a vague reporting expectation into explicit fields, checks, and follow-up questions.
- A contributor can see what is missing without receiving a productivity or performance score.
- An unverifiable claim stays `unknown` instead of becoming a confident but false success.
- A policy can be replayed through a stable digest and deterministic engine.
- A connector can draft an approval-gated plan without network access or invented duration.

It is not yet a production platform. There is no multi-tenant service, authentication model, retention service, live connector, large policy registry, external contributor base, or real-world outcome study. The five persona evaluations validate product contracts and safety boundaries; they do not prove organizational ROI.

The correct current claim is therefore:

> This is a promising, auditable kernel for evidence workflows—not a finished replacement for Jira, a performance-management system, or an enterprise governance platform.

## 3. Where the large value can emerge

| Value layer | What it provides | Potential | What unlocks it |
|---|---|---:|---|
| 1. Better templates | More useful weekly updates and briefs | Moderate | Good starter packs and low-friction UX |
| 2. Policy-as-code for artifacts | Versioned, testable criteria for work outputs | High | Typed schema, conformance tests, explainable results |
| 3. Evidence contract protocol | A common result shape across tools and teams | Very high | Stable API, event model, policy digest, connector SDK |
| 4. Open policy-pack ecosystem | Domain experts share reusable workflows | Very high | Registry, pack review, fixtures, compatibility rules |
| 5. Trustworthy workflow infrastructure | Systems can route evidence without guessing or surveilling | Very high | Privacy, provenance, approval gates, audit receipts, real integrations |

The project should optimize for layers 2–4. Layer 1 is the wedge; layer 5 is the long-term ambition.

## 4. Positioning against adjacent projects

This project should complement established infrastructure rather than pretend to replace it.

- [Open Policy Agent](https://www.openpolicyagent.org/docs) is a general-purpose policy decision engine. `evidence-workflows` sits upstream: it focuses on policy authoring conversations, human-completable evidence artifacts, uncertainty, and next questions. An OPA adapter could become a future enforcement path for selected machine-checkable rules.
- [OpenFeature](https://openfeature.dev/docs/reference/intro/) demonstrates the value of a vendor-neutral API plus provider adapters. `evidence-workflows` can use the same pattern for policy packs and connectors: a stable core contract with Jira, GitHub, chat, CI, and internal-system adapters.
- [OpenLineage](https://openlineage.io/docs/) demonstrates how an open metadata model and shared integrations can create value beyond one tool. A future evidence event could carry provenance facets such as source, owner, policy version, review state, and retention class.
- Jira and similar systems remain systems of record. This project should add semantic completion and evidence routing rather than compete with their issue/worklog storage.
- LLMs may improve wording, extraction, or conversational UX later, but the safety-critical decision kernel should remain deterministic and able to run without a model.

## 5. Why open source matters

The main value is unlikely to come from one company owning a hidden rubric. It comes from shared, inspectable semantics.

Open source enables:

1. **Trust:** people can inspect what a policy checks and what it refuses to infer.
2. **Portability:** teams are not forced to encode their working agreement inside one vendor’s workflow product.
3. **Domain contribution:** an incident responder, data scientist, researcher, or manufacturing engineer can contribute a pack without changing the engine.
4. **Independent validation:** communities can challenge false positives, privacy risks, and culturally narrow assumptions.
5. **Interoperability:** connectors can compete while sharing a stable result and policy contract.
6. **Institutional memory:** policy versions, fixtures, and digests preserve why a workflow changed.

The open-source flywheel is:

```text
new domain need
  → policy pack + fixtures
  → reusable checks and questions
  → connector adoption
  → more edge cases and conformance tests
  → stronger shared protocol
```

## 6. Highest-leverage roadmap

### Phase A — Trust kernel (`0.2`)

Goal: make the deterministic core hard to misuse.

- Publish a formal JSON Schema for policies, artifacts, results, and connector plans.
- Add policy expiry, owner, review history, compatibility, and migration metadata.
- Expand typed checks conservatively: provenance, numeric claims, source freshness, and explicit lifecycle transitions.
- Add pack conformance tests, negative fixtures, red-team cases, and a false-block benchmark.
- Define privacy profiles, retention hooks, deletion semantics, and redaction extension points.
- Keep `unknown`, `not_applicable`, and `needs_clarification` distinct in every adapter.

### Phase B — Contributor experience (`0.3`)

Goal: make the interview easier than writing a vague report.

- Add a small local web UI and chat-friendly one-question-at-a-time flow.
- Preserve the exact policy version and reason for every follow-up question.
- Support answer revision, partial saves, localization, accessibility, and structured citations.
- Add diff views showing what changed between two artifact submissions.
- Provide policy-authoring workshops/templates for leaders and domain maintainers.

### Phase C — Interoperability (`0.4`–`0.5`)

Goal: make one policy useful in the tools where work already happens.

- Ship an adapter SDK and a versioned connector protocol.
- Add read-only Jira, GitHub, Slack/Teams, Notion, CI, and data-platform adapters first.
- Keep write operations behind explicit plans, approval, apply, and read-back receipts.
- Add signed result envelopes, idempotency keys, remote revision checks, and webhook events.
- Integrate provenance concepts so every claim can point back to a safe source.

### Phase D — Open ecosystem (`0.6`–`0.9`)

Goal: let many people create value without fragmenting the semantics.

- Create a searchable policy-pack registry with owners, versions, licenses, privacy notes, and supported engine versions.
- Add pack scorecards: clarity, burden, false-block rate, unknown handling, sensitive-data behavior, and maintenance status.
- Add a conformance suite that adapters and alternative implementations can run.
- Publish anonymized or synthetic benchmark corpora for domain packs.
- Establish review guidelines and a lightweight governance model for the core schema.

### Phase E — Production boundary (`1.0`)

Goal: support organizations that need a service without closing the core.

- Optional hosted control plane with tenant isolation, RBAC, audit logs, retention controls, and regional data boundaries.
- Queue/retry behavior and observable connector runs.
- Enterprise identity integrations and policy approval workflow.
- Stable SDKs for Python, TypeScript, and HTTP/OpenAPI clients.
- Clear open-core boundary: the policy format, engine contract, pack conventions, and conformance tests remain open.

## 7. The five biggest future merits

### A. It can reduce coordination ambiguity

Many teams do not lack activity data; they lack a shared definition of what information is decision-useful. A policy interview can surface that definition before a reporting workflow is automated.

### B. It can make automation safer

Most workflow automation fails in one of two ways: it silently guesses, or it acts on an opaque score. Explicit `unknown`, typed checks, redaction, and approval-gated connectors create a safer boundary for automation.

### C. It can turn domain knowledge into reusable infrastructure

A good incident policy or experiment policy should not be rewritten by every team. Packs let domain experts publish a reusable starting point while keeping local policy ownership visible.

### D. It can become a neutral interoperability layer

If policy and result semantics are stable, the same artifact can move between a local CLI, Jira, GitHub, chat, CI, and a future internal service without re-implementing the meaning each time.

### E. It can preserve organizational learning

Versioned policies, fixtures, results, and receipts can explain how a team’s operating model changed. That is more durable than a dashboard metric or an undocumented manager preference.

## 8. Success metrics for the project

These are proposed targets, not current achievements.

- **Adoption:** three independent teams use the engine; ten external policy packs exist.
- **Contributor value:** most first-pass artifacts become `ready` or receive a small, actionable question set rather than a long form.
- **Trust:** every result identifies its policy version/digest; no fixture leaks sensitive patterns; no adapter bypasses approval for writes.
- **Quality:** false-block and false-ready rates are measured on public synthetic benchmarks, not hidden anecdotes.
- **Interoperability:** at least three independent connectors consume the same result contract.
- **Sustainability:** multiple maintainers review core schema changes; packs declare owners and review dates.

The most important metric is not the number of worklogs created. It is whether teams make better, faster, and more explainable decisions with less ambiguity and less reporting burden.

## 9. Main risks and countermeasures

| Risk | What failure looks like | Countermeasure |
|---|---|---|
| Surveillance drift | A “worklog” becomes a hidden employee score | Make non-goals executable, visible, and reviewable; reject HR scoring packs |
| Bureaucracy | Contributors spend more time answering than deciding | Measure question count and completion burden; default to minimum evidence |
| False certainty | A weak URL or confident sentence becomes `pass` | Preserve `unknown`; require evidence types and source freshness |
| Policy fragmentation | Every team invents incompatible fields | Versioned schema, pack registry, conformance tests, migration rules |
| Connector lock-in | One vendor’s API becomes the product model | Keep connectors thin and the core contract vendor-neutral |
| AI overreach | An LLM invents evidence or silently changes policy meaning | Keep evaluation deterministic; make model use optional and bounded |
| Governance capture | A small group changes the standard invisibly | Public policy diffs, owners, review dates, changelog, and community review |

## 10. Contribution paths with real leverage

The most valuable contributions are not only more code:

- Add a domain pack with positive, missing, unverifiable, sensitive, and in-progress fixtures.
- Add a typed check with clear semantics, tests, privacy analysis, and migration behavior.
- Build a read-only connector and prove its provenance mapping.
- Improve the interview UX without increasing the required evidence burden.
- Add accessibility, localization, and plain-language prompts.
- Create adversarial benchmarks for false certainty, surveillance drift, and sensitive-data leakage.
- Review policies from a different domain or cultural context.

## 11. Bottom line

The project has modest immediate value as a local policy/checking toolkit and significant potential value as an open evidence-workflow protocol. The upside is large because the same contract can be reused by many teams and systems. The upside is not automatic: it depends on trust, low burden, strong interoperability, public packs, measurable quality, and a hard boundary against covert performance management.

The strategic goal should be:

> From “a better worklog checker” to “an open, auditable contract layer for decision-useful work evidence.”
