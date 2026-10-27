# Security and privacy

The toolkit reads only the local platform and the presence of an allowlist of environment variables. It does not inspect browser cookies, Keychain entries, shell history, Claude settings, or token files. It does not authenticate, install software, alter network settings, or initiate purchases.

Calendar output is written to standard output. Shell redirection creates the destination file; the program does not import it into Calendar or change a subscription. No telemetry is collected.

Do not post secrets or personal account evidence in public issues. For a code vulnerability, use the repository's private vulnerability reporting feature if enabled. If it is unavailable, open a minimal issue asking for a private reporting channel without disclosing exploit details or sensitive data. For a Claude account problem, contact Anthropic support directly.

If a credential is exposed, revoke it with its issuer, review account activity, and remove it from public history as appropriate. Deleting the latest copy of a file does not remove earlier Git commits.
