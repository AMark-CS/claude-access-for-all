# Claude Access for All

**Frontier intelligence should serve humanity, in every corner of the world.**

An open, English-language field guide and local toolkit for accessing Claude Code on macOS: subscription choices, network reliability, billing hygiene, account security, and recovery.

## Why this exists

The next great scientific idea may come from a student with an aging laptop. The next useful piece of software may begin in a small town, far from a technology hub. Talent is everywhere. Access to the tools that multiply it is still uneven.

We believe AI should benefit all of humanity. The ability to learn, build, and participate in the future should reach people across borders, languages, and economic circumstances. That includes developers in corners of the world where access is currently restricted, communities overlooked by product rollouts, and people for whom a failed subscription is a meaningful financial loss.

Claude Code is the starting point for this project because we want more people to experience frontier AI in their daily work. Our ambition is a world where the best available models are within everyone's reach. We treat that as a mission, not a permanent benchmark ranking for any single model or company.

Open knowledge can reduce confusion, expose misleading promises, help people protect their money and accounts, and make barriers visible to the people who can remove them. We hope this repository becomes a small piece of that shared infrastructure.

## Start here

1. Read [availability and access paths](docs/availability.md) before spending money.
2. Follow the [macOS quickstart](docs/macos-quickstart.md).
3. Choose and manage a plan with the [subscription playbook](docs/subscriptions.md).
4. Diagnose connectivity with the [network and “clean IP” guide](docs/network.md).
5. Protect your account with the [account continuity guide](docs/account-continuity.md).
6. Review the [client privacy inspector](docs/privacy-inspector.md) for CLI, Desktop, and web.
7. Use the [troubleshooting decision table](docs/troubleshooting.md) when something breaks.

## What you get

| Area | Practical outcome |
| --- | --- |
| macOS setup | Install, authenticate, and verify your billing route |
| Network reliability | Separate proxy, TLS, service, and account problems |
| Subscription management | Record billing ownership and review renewals |
| Account continuity | Secure access, preserve work, and prepare an appeal |
| Local tools | Offline diagnostics, scoped launchers, browser signal inspector, and calendar reminder |
| Evidence | Dated official sources and a contribution standard |

## Install and run

Requires macOS, Node.js 18+, Python 3.9+, and Git for the GitHub install. Install Claude Code or Claude Desktop separately when needed. Install the CLI from the npm registry or directly from GitHub.

Run the interactive menu without a permanent install:

```sh
npx --yes claude-access-for-all
```

Or install the command globally:

```sh
npm install -g claude-access-for-all
claude-access
```

Choose an action from the interactive menu, or call one directly:

```sh
claude-access doctor
claude-access audit
claude-access cli --timezone UTC
claude-access app --timezone UTC
claude-access web --browser chrome --timezone UTC
claude-access inspect
claude-access reminder --renewal 2026-12-01 --days-before 3 > renewal.ics
open renewal.ics
```

To install directly from GitHub, use `npm install -g github:AMark-CS/claude-access-for-all`. Use `claude-access help` to see the complete command list. `inspect` opens the local graphical browser inspector in your default browser. To check a separate browser profile, open its local file in that profile instead; see the [privacy inspector guide](docs/privacy-inspector.md).

For the calendar reminder, replace the example date with the next billing date shown by your billing provider. The file contains one all-day review event with an alert; import it into Apple Calendar and check your notification settings. It neither cancels nor renews anything, and must be regenerated when the billing date changes.

The diagnostics run offline and do not print environment-variable values. The scoped launchers request process-local timezone and language settings; Desktop and browsers may behave differently. The browser launcher opens Claude in a separate profile and prints its private data directory. Review the [privacy guide](docs/privacy-inspector.md) for limitations before use.

To run the source version directly without npm, use `python3 tools/access.py doctor` or `python3 tools/privacy.py audit` from a clone. Review the short [source](tools/access.py) before running it.

## Honest boundaries

Anthropic currently limits availability by location. A working connection or successful payment does not establish eligibility. This project cannot grant access, reverse a suspension, or guarantee that an account stays active. See the [official availability list](https://support.claude.com/en/articles/8461763-where-can-i-access-claude).

We document practical access issues and advocate broader availability. We do not sell accounts, proxy subscriptions, credentials, or guarantees of immunity from account review. No VPN vendor, IP reputation score, or “account warming” ritual is endorsed as a solution to eligibility restrictions.

## Help build this

Contribute a reproducible fix, a clearer explanation, an accessibility improvement, or a dated policy correction. Please read [CONTRIBUTING.md](CONTRIBUTING.md), the [evidence register](docs/sources.md), and [SECURITY.md](SECURITY.md) first. Never put account identifiers, IP addresses, receipts, tokens, or payment details in public issues.

Potential next steps: a macOS menu bar companion, additional billing-provider walkthroughs, and a structured history of access barriers. These are roadmap ideas.

Independent community project. Not affiliated with or endorsed by Anthropic. Claude and Claude Code are their respective owners' trademarks. MIT licensed. Official sources last reviewed **October 27, 2026**; recheck them before purchasing.
