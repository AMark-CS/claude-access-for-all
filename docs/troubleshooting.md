# Troubleshooting decision table

Use the exact error and the smallest relevant check. Redact screenshots before sharing them.

| Symptom | First check | Next action |
| --- | --- | --- |
| `claude` not found | Installation method and PATH | Run the official setup checks |
| Paid account appears free | Signed-in account and provider receipt | Check the purchase channel before buying again |
| Unexpected API charges | `/status`, API-key presence | Remove an unintended override; review Console billing |
| Login callback never completes | Local browser/terminal context | Follow the manual authentication flow in official troubleshooting |
| TLS failure | System clock and authorized CA setup | Ask IT to fix trust configuration |
| Browser works, CLI times out | Proxy environment in that shell | Compare process configuration privately |
| Model unavailable | Current entitlement and selected model | Choose an available model or contact your administrator |
| Usage limit | Account's displayed limit and reset | Wait for reset or evaluate a tier change |
| Widespread errors | Official status page | Check incident updates before changing local settings |
| Region unavailable | Official availability list | Request clarification if apparently misclassified |
| Account disabled | Restriction notice | Use the official appeal and review billing separately |
| Payment declined | Checkout details and issuer response | Ask issuer/provider; avoid repeated blind retries |

References: [installation/authentication troubleshooting](https://support.claude.com/en/articles/14552646-troubleshoot-claude-code-installation-and-authentication), [API-key precedence](https://support.claude.com/en/articles/12304248-manage-api-key-environment-variables-in-claude-code), [service status](https://status.claude.com/), and [appeals](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals).

The local doctor does not make network requests or inspect account state. Its successful completion is not a service-health or eligibility result.
