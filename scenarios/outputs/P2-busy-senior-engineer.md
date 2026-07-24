# Evidence workflow result: `reporting.technical-weekly-update`

- Status: **needs_clarification**
- Policy version: `0.1.0`
- Policy digest: `5e976f8058d4583f0f445c7dbb49106342b9a175de9153eada7dd56972ee2f9b`
- Engine version: `0.1.0`

## Artifact (redacted)

```json
{
  "current_state": "알람 noise를 줄이기 위해 aggregation rule을 손봤다.",
  "impact_or_risk": "오탐은 줄 수 있지만 신규 장애를 놓칠 가능성을 다음 주에 확인해야 한다.",
  "next_action": {
    "action": "새 rule을 staging에서 검증"
  },
  "period": "2026-07-20 ~ 2026-07-24"
}
```

## Checks

| Check | Status | Blocking | Message |
|---|---|---:|---|
| `period-present` | `pass` | True | 업데이트 기간이 필요합니다. |
| `current-state-present` | `pass` | True | 현재 상태가 필요합니다. |
| `evidence-reference` | `fail` | True | 검증 가능한 URL, Jira key, PR/커밋 참조가 필요합니다. |
| `impact-or-risk-present` | `pass` | True | 영향 또는 리스크가 필요합니다. |
| `next-action-present` | `pass` | True | 다음 행동이 필요합니다. |
| `next-action-owner-present` | `fail` | True | 다음 행동의 책임자가 필요합니다. |
| `next-action-due-date` | `fail` | True | 다음 행동의 확인 예정일이 ISO 날짜로 필요합니다. |
| `no-sensitive-data` | `pass` | True | 개인정보와 credential은 artifact에서 제거해야 합니다. |

## Follow-up questions

- **evidence** — 주장을 확인할 수 있는 Jira 이슈, PR, 커밋, 대시보드 URL 중 하나를 남겨 주세요. (검증 가능한 URL, Jira key, PR/커밋 참조가 필요합니다.)
- **next_action.owner** — 다음 행동의 책임자 또는 팀을 적어 주세요. (다음 행동의 책임자가 필요합니다.)
- **next_action.due_date** — 다음 행동의 확인 예정일을 ISO 날짜로 적어 주세요. (다음 행동의 확인 예정일이 ISO 날짜로 필요합니다.)

## Warnings

No warnings.

## Synthetic evaluation

- Score: **100 / 100**
- Overall: **pass**
- `status_matches`: pass — expected needs_clarification, got needs_clarification
- `check_contract`: pass — required check statuses match the case contract
- `actionable_questions`: pass — every follow-up question has a field, prompt, and reason
- `no_sensitive_leak`: pass — no email/token pattern appears in the generated result
- `uncertainty_is_honest`: pass — unverified claims remain unknown
- `redaction_safety`: pass — sensitive input was redacted before output
- `progress_is_not_failure`: pass — in-progress work is explicit and not forced into a completed result
- `no_hr_scoring`: pass — output contains no productivity or attendance score
