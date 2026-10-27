# Security and privacy

The offline diagnostics read the local platform, timezone names, and the presence of an allowlist of environment variables. It does not inspect browser cookies, Keychain entries, shell history, Claude settings, or token files. The optional launchers start locally installed apps with requested process-scoped locale and timezone settings. The opt-in autostart command installs a user LaunchAgent that requests Claude at login; its disable command removes that item without quitting Claude. The web launcher opens Claude and creates or reuses a dedicated profile. The local browser inspector collects browser-visible signals only within the page. The tools do not authenticate on your behalf, install software, alter system network settings, or initiate purchases.

Calendar output is written to standard output. Shell redirection creates the destination file; the program does not import it into Calendar or change a subscription. No telemetry is collected.

Do not post secrets or personal account evidence in public issues. For a code vulnerability, use the repository's private vulnerability reporting feature if enabled. If it is unavailable, open a minimal issue asking for a private reporting channel without disclosing exploit details or sensitive data. For a Claude account problem, contact Anthropic support directly.

If a credential is exposed, revoke it with its issuer, review account activity, and remove it from public history as appropriate. Deleting the latest copy of a file does not remove earlier Git commits.
