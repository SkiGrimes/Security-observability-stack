# Framework Mapping

How the two detections in this lab map to MITRE ATT&CK and to the compliance controls that motivated them.

## MITRE ATT&CK

| Attack scenario | Technique | Detection signal | Data source |
|---|---|---|---|
| Volumetric DDoS (app-layer HTTP flood) | [T1499.002 — Endpoint DoS: Service Exhaustion Flood](https://attack.mitre.org/techniques/T1499/002/) | Sustained request-rate spike above baseline | `http_requests_total` (counter) |
| Volumetric DDoS (network angle) | [T1498 — Network Denial of Service](https://attack.mitre.org/techniques/T1498/) | Same volumetric signal, viewed as availability impact | `http_requests_total`, Node Exporter |
| Credential stuffing | [T1110.004 — Brute Force: Credential Stuffing](https://attack.mitre.org/techniques/T1110/004/) | Login attempts/min above threshold, high `401` rate | `login_attempts_total` (counter), HTTP status |

**Detection philosophy:** aggregate, rate-based alerting rather than per-request blocking. This flags the *pattern* (volume anomaly) without adding latency or a failure point to legitimate traffic — the app still authenticates real users normally during a credential-stuffing event.

## NIST Cybersecurity Framework 2.0

| Function | Category | How this lab satisfies it |
|---|---|---|
| Detect | `DE.CM` — Continuous Monitoring | Prometheus scrapes every 15s; Grafana alert rules evaluate continuously |
| Detect | `DE.AE` — Adverse Event Analysis | Alert evaluation graphs + dashboard panels distinguish attack from baseline |

## GLBA Safeguards Rule (16 CFR Part 314)

| Control | Requirement | How this lab satisfies it |
|---|---|---|
| §314.4(h) | Continuous monitoring or periodic testing of key controls protecting customer financial data | Automated, auditable, real-time detection of two high-rated threat scenarios where none previously existed |

## NIST SP 800-30

The two scenarios were not chosen arbitrarily — they were selected via an SP 800-30 risk assessment (threat sources, vulnerabilities, likelihood/impact rating), which rated application-availability DDoS and auth-endpoint credential stuffing as the two highest-probability threats to the environment.

## Residual risk (documented, not hidden)

- Thresholds are calibrated on synthetic k6 traffic, not a production baseline — requires re-tuning against 1–2 weeks of real traffic.
- Single notification contact point is a SPOF — production should add a redundant channel.
