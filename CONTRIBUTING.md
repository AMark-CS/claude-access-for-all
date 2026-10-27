# Contributing

All maintained documentation and tool output are in English. Keep explanations welcoming, precise, and useful to newcomers.

For a policy correction, include the official URL, review date, changed claim, and affected guide. For a troubleshooting fix, include the macOS version, installation method, symptom, minimal reproduction, expected outcome, and redacted observed outcome. Label claims Official, Observed, or Unverified using the evidence register.

Do not submit credentials, account identifiers, raw IP addresses, billing documents, residential proxy advertisements, referral links, guaranteed-unban offers, or fabricated success rates. Describe general findings without identifying individual users. Treat people respectfully regardless of nationality, location, language, or technical experience.

Run checks before opening a pull request:

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_docs.py
```

Prefer the Python standard library and keep the doctor offline. Changes to network behavior must document the destination and data sent, and require an explicit user action. Changes to billing integrations must explain credential handling and financial side effects.
