# Evidence workflow result: `analysis.data-experiment`

- Status: **ready**
- Policy version: `0.1.0`
- Policy digest: `141f8d6136b3a456816d58555b71174d147240ee95989f3b3c5749a617172425`
- Engine version: `0.1.0`

## Artifact (redacted)

```json
{
  "data_scope": "파일럿 라인 B의 2026-07-15~2026-07-22 이벤트와 실제 점검 기록",
  "evidence": "https://example.invalid/notebooks/anomaly-feature-v2",
  "experiment_question": "새 anomaly feature가 기존 rule보다 조기 경보를 제공하는가?",
  "hypothesis": "false positive를 늘리지 않고 평균 15분 먼저 경보할 수 있다.",
  "method": "시간 순서 split으로 기존 rule과 신규 feature의 lead time 및 false positive 비교",
  "next_experiment": {
    "action": "점검 기록 6건을 추가 라벨링하고 false positive를 재계산",
    "due_date": "2026-07-29",
    "owner": "Applied Research"
  },
  "phase": "in_progress"
}
```

## Checks

| Check | Status | Blocking | Message |
|---|---|---:|---|
| `phase-present` | `pass` | True | 실험 단계가 필요합니다. |
| `phase-allowed` | `pass` | True | 실험 단계는 in_progress, completed, blocked 중 하나여야 합니다. |
| `experiment-question-present` | `pass` | True | 분석 질문이 필요합니다. |
| `hypothesis-present` | `pass` | True | 검증할 가설이 필요합니다. |
| `data-scope-present` | `pass` | True | 데이터 범위가 필요합니다. |
| `method-present` | `pass` | True | 분석 방법이 필요합니다. |
| `evidence-reference` | `pass` | True | 재현 가능한 URL, Jira key, PR, 또는 커밋 참조가 필요합니다. |
| `result-required-when-complete` | `not_applicable` | True | 완료 또는 blocked 단계에는 관찰 결과가 필요합니다. |
| `next-experiment-present` | `pass` | True | 다음 실험 또는 확인 행동이 필요합니다. |
| `next-experiment-owner-present` | `pass` | True | 다음 실험의 책임자가 필요합니다. |
| `next-experiment-due-date` | `pass` | True | 다음 실험의 확인 예정일이 ISO 날짜로 필요합니다. |
| `no-sensitive-data` | `pass` | True | 분석 artifact에는 개인정보와 credential이 없어야 합니다. |

## Follow-up questions

No follow-up questions.

## Warnings

- 아직 진행 중인 실험입니다. 최종 결과 대신 다음 확인 행동을 명시한 상태로 유지합니다.

## Synthetic evaluation

- Score: **100 / 100**
- Overall: **pass**
- `status_matches`: pass — expected ready, got ready
- `check_contract`: pass — required check statuses match the case contract
- `actionable_questions`: pass — every follow-up question has a field, prompt, and reason
- `no_sensitive_leak`: pass — no email/token pattern appears in the generated result
- `uncertainty_is_honest`: pass — unverified claims remain unknown
- `redaction_safety`: pass — sensitive input was redacted before output
- `progress_is_not_failure`: pass — in-progress work is explicit and not forced into a completed result
- `no_hr_scoring`: pass — output contains no productivity or attendance score
