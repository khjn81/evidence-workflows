# Synthetic persona evaluation

This report evaluates the evaluator on synthetic personas. It is not an employee-performance assessment.

- Cases: **5**
- Passed: **5 / 5**
- Average score: **100.0 / 100**

| Case | Persona | Expected | Actual | Score | Overall |
|---|---|---|---|---:|---|
| `P1-careful-data-analyst` | 꼼꼼한 데이터 분석가 | `ready` | `ready` | 100 | pass |
| `P2-busy-senior-engineer` | 시간이 부족한 시니어 엔지니어 | `needs_clarification` | `needs_clarification` | 100 | pass |
| `P3-optimistic-manager` | 성과를 크게 말하는 리더 | `unable_to_determine` | `unable_to_determine` | 100 | pass |
| `P4-sensitive-incident-responder` | 민감정보를 붙여 넣은 장애 대응자 | `needs_clarification` | `needs_clarification` | 100 | pass |
| `P5-in-progress-junior-researcher` | 아직 결론이 없는 주니어 연구자 | `ready` | `ready` | 100 | pass |

## Interpretation

- A pass means the deterministic engine met the synthetic case contract; it does not validate organizational usefulness.
- A ready result still requires a human to decide whether the artifact belongs in the target workflow.
- unknown is intentionally preserved when a claim lacks a verifiable reference.
