# Network reliability and the “clean IP” question

Last reviewed: October 27, 2026. Technical reference: [official network configuration](https://code.claude.com/docs/en/network-config).

## Define the problem before buying a solution

“Clean IP” is a marketing phrase, not a standardized eligibility certificate. An address can have different reputation scores in different databases. Neither those scores nor a residential address establish that Anthropic will accept an account. This project has no verified threshold that predicts suspension or signup success.

For ordinary troubleshooting, focus on a connection you trust, correctly configured DNS, valid TLS, and a route you can explain to your network administrator. Public IP geolocation databases can disagree. When your actual eligible location is misclassified, request support review with minimal private evidence rather than treating a vendor's country label as definitive.

## Inspect locally

Run `python3 tools/access.py doctor` first. It reports presence of common environment overrides without printing their values. On macOS, you can additionally inspect the system proxy configuration locally:

```sh
scutil --proxy
```

Do not publish that raw output: it may reveal internal infrastructure. Browser success does not establish that a terminal process uses the same route. Check which shell and app you launched before changing settings.

## Configure an authorized proxy

For a proxy you operate or your organization provides, use its actual HTTP proxy endpoint in the shell that launches Claude Code:

```sh
# Example only: replace with your authorized proxy endpoint.
export HTTPS_PROXY=http://127.0.0.1:8080
claude
```

Claude Code documents HTTP/HTTPS proxy variables and does not support SOCKS directly. Restart the relevant terminal session after changing its environment. For Desktop sessions, consult the official page's settings-scope rules rather than assuming shell exports reach every app workflow.

For an enterprise inspection certificate, ask IT for the authorized CA configuration. Keep TLS validation enabled. Do not install an unknown root certificate supplied by an account reseller.

## Test one symptom at a time

Use a request without account credentials to check basic HTTPS behavior:

```sh
curl -I --connect-timeout 5 --max-time 15 https://claude.ai
```

This sends your ordinary network metadata, including the connection's source IP, to the destination and any configured proxy. It is optional and is not run by the doctor. An HTTP response establishes only that this request received a response; it does not validate the full login, subscription, API, or streaming path. A 403 alone cannot distinguish account policy from routing or other denials.

| Observation | Investigate next |
| --- | --- |
| DNS or connection timeout | Local network, captive portal, proxy endpoint, firewall |
| Certificate error | Clock, certificate chain, authorized corporate inspection |
| Browser works, terminal fails | Process-specific proxy and certificate configuration |
| Login succeeds, model request fails | Authentication, entitlement, service status, actual error |
| Official region restriction | Eligibility and support review |

Before paying a network vendor, ask who operates the exit, what traffic is logged, whether TLS is intercepted, how credentials are handled, and what refund terms apply. Avoid sellers claiming guaranteed account safety or asking for Claude cookies. A network purchase cannot promise account eligibility.
