# Evidence workflow result: `operations.incident-investigation`

- Status: **needs_clarification**
- Policy version: `0.1.0`
- Policy digest: `d5fc3867ae3fb0b4db719e68af1f1620be9c769a93484518bc6a56bf8b98c04e`
- Engine version: `0.1.0`

## Artifact (redacted)

```json
{
  "api_token": "<redacted:sensitive_field>",
  "customer_email": "<redacted:email>",
  "evidence": [
    "https://example.invalid/incidents/INC-77",
    "INC-77"
  ],
  "impact": "라인 A 작업 지시 조회 p95가 2.4초에서 9.8초로 증가했으며 영향 설비는 12대다.",
  "mitigation": "느린 query를 feature flag로 우회하고 read replica를 증설했다.",
  "next_action": {
    "action": "PII가 제거된 재현 로그로 query plan을 검토",
    "due_date": "2026-07-25",
    "owner": "SRE"
  },
  "summary": "2026-07-23 14:10부터 작업 지연이 증가했고 <redacted:email> 계정에서도 재현되었다."
}
```

## Checks

| Check | Status | Blocking | Message |
|---|---|---:|---|
| `summary-present` | `pass` | True | 장애 요약이 필요합니다. |
| `impact-present` | `pass` | True | 장애 영향 범위가 필요합니다. |
| `evidence-reference` | `pass` | True | 안전한 로그, 모니터링, 이슈, 또는 재현 근거가 필요합니다. |
| `mitigation-present` | `pass` | True | 현재 완화 조치가 필요합니다. |
| `next-action-present` | `pass` | True | 다음 안전 조치가 필요합니다. |
| `next-action-owner-present` | `pass` | True | 다음 안전 조치의 책임자가 필요합니다. |
| `next-action-due-date` | `pass` | True | 다음 안전 조치의 확인 예정일이 ISO 날짜로 필요합니다. |
| `no-sensitive-data` | `fail` | True | 장애 artifact에는 고객 식별자와 credential이 없어야 합니다. |

## Follow-up questions

- **evidence** — 고객 식별자와 credential을 제거한 근거 참조로 다시 남겨 주세요. (장애 artifact에는 고객 식별자와 credential이 없어야 합니다.)

## Warnings

- 민감정보 패턴은 결과 출력에서 자동 마스킹되었습니다. 원문을 외부 시스템에 전송하지 마세요.

## Redactions

3 sensitive pattern(s) were redacted from the report.

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
