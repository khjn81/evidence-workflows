# Evidence workflow result: `communication.presentation-brief`

- Status: **unable_to_determine**
- Policy version: `0.1.0`
- Policy digest: `12f57e90fb4e23cd7fb997103678b194f9a6b6b28eb82737d6e3b15e63c27e7d`
- Engine version: `0.1.0`

## Artifact (redacted)

```json
{
  "ask": "3개 사이트로 파일럿을 확대할 예산 승인",
  "audience": "사업부 리더와 재무 파트너",
  "decision": "다음 분기 현장 AI 파일럿 예산을 승인할지 결정",
  "evidence": "사용자들이 좋아했고 전보다 빨라진 것 같다.",
  "key_claims": [
    "현장 사용자 반응이 매우 좋았다.",
    "분석 속도가 크게 개선되었다."
  ]
}
```

## Checks

| Check | Status | Blocking | Message |
|---|---|---:|---|
| `decision-present` | `pass` | True | 발표가 지원할 결정이 필요합니다. |
| `audience-present` | `pass` | True | 핵심 청중이 필요합니다. |
| `claims-present` | `pass` | True | 핵심 주장이 필요합니다. |
| `evidence-reference` | `unknown` | True | 핵심 주장을 확인할 수 있는 근거 참조가 필요합니다. |
| `ask-present` | `pass` | True | 청중에게 요청할 다음 결정이나 행동이 필요합니다. |
| `no-sensitive-data` | `pass` | True | 발표 근거에 개인정보와 credential이 없어야 합니다. |

## Follow-up questions

- **evidence** — 각 주장을 확인할 수 있는 데이터나 원문 참조를 남겨 주세요. (확인 가능한 근거가 없어 판단할 수 없습니다: 핵심 주장을 확인할 수 있는 근거 참조가 필요합니다.)

## Warnings

No warnings.

## Synthetic evaluation

- Score: **100 / 100**
- Overall: **pass**
- `status_matches`: pass — expected unable_to_determine, got unable_to_determine
- `check_contract`: pass — required check statuses match the case contract
- `actionable_questions`: pass — every follow-up question has a field, prompt, and reason
- `no_sensitive_leak`: pass — no email/token pattern appears in the generated result
- `uncertainty_is_honest`: pass — unverified claims remain unknown
- `redaction_safety`: pass — sensitive input was redacted before output
- `progress_is_not_failure`: pass — in-progress work is explicit and not forced into a completed result
- `no_hr_scoring`: pass — output contains no productivity or attendance score
