# Evidence workflow result: `analysis.data-experiment`

- Status: **ready**
- Policy version: `0.1.0`
- Policy digest: `141f8d6136b3a456816d58555b71174d147240ee95989f3b3c5749a617172425`
- Engine version: `0.1.0`

## Artifact (redacted)

```json
{
  "data_scope": "2026-07-01~2026-07-21, 라인 A 센서 18개, 재시작 10분 구간 제외 여부를 별도 비교",
  "evidence": [
    "https://example.invalid/analysis/line-a-missingness",
    "AN-184"
  ],
  "experiment_question": "라인 A의 센서 결측이 특정 교대조에 집중되는가?",
  "hypothesis": "야간 교대의 네트워크 재시작 직후 결측률이 높을 것이다.",
  "method": "교대조별 결측률과 재시작 이벤트를 join하고 95% bootstrap 구간을 비교",
  "next_experiment": {
    "action": "네트워크 재시작 전후 30분 구간으로 민감도 분석을 재실행",
    "due_date": "2026-07-31",
    "owner": "Data Platform"
  },
  "phase": "completed",
  "result": "야간 결측률 중앙값이 주간보다 3.1%p 높았지만 표본 수가 작아 원인으로 확정하지 않았다."
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
| `result-required-when-complete` | `pass` | True | 완료 또는 blocked 단계에는 관찰 결과가 필요합니다. |
| `next-experiment-present` | `pass` | True | 다음 실험 또는 확인 행동이 필요합니다. |
| `next-experiment-owner-present` | `pass` | True | 다음 실험의 책임자가 필요합니다. |
| `next-experiment-due-date` | `pass` | True | 다음 실험의 확인 예정일이 ISO 날짜로 필요합니다. |
| `no-sensitive-data` | `pass` | True | 분석 artifact에는 개인정보와 credential이 없어야 합니다. |

## Follow-up questions

No follow-up questions.

## Warnings

No warnings.

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
