# Client privacy inspector and scoped launchers

Reviewed October 27, 2026. This toolkit borrows the idea of independently inspecting timezone, language, browser identity, and fonts from [Fuck Claude](https://fuck-claude.com/). Its scoring and claims are third-party interpretations, not verified Anthropic enforcement rules. The CLI adapts its timezone and offset scoring rules with attribution; the limited result is not a ban prediction. See the bundled [MIT notice](../third-party/FuckClaude-LICENSE.txt).

Each client has its own process and network path. A change applied to Terminal does not necessarily affect Desktop or an existing browser. Nothing here changes the macOS system timezone, system language, global proxy settings, the installed Claude apps, or existing browser profiles.

## Local partial score

Run `claude-access score` in the terminal to score the current process timezone and current UTC offset. The result uses the reference project's 24-point timezone rule and 3-point offset rule. It shows earned points and only the maximum for signals actually available, so it is **not** the reference browser's 100-point score. Other reference signals require a browser and are marked unmeasured; IP, credentials, billing and account state are not checked. A missing timezone is excluded rather than treated as zero. `TZ=America/Los_Angeles claude-access score` checks the requested launcher timezone in a child process, not your existing browser or Desktop application. Rules are third-party heuristics and do not establish an Anthropic enforcement decision.

## 1. Claude Code CLI

```sh
python3 tools/privacy.py audit
python3 tools/privacy.py cli --timezone America/Los_Angeles --locale en_US.UTF-8
# Pass CLI arguments after --, for example:
python3 tools/privacy.py cli --timezone America/Los_Angeles -- --version
```

The audit reports the current shell's timezone names and whether known locale, routing, and authentication environment variables are set. It does not print their values. Treat even local timezone output as private. It cannot inspect values in Claude settings, other running processes, system proxies, DNS, or server-side checks.

The launcher defaults to `America/Los_Angeles` and starts `claude` with `TZ`, `LANG`, and `LC_ALL` changed only in the new process and its child processes. Select another installed IANA timezone with `--timezone`, and another available locale with `--locale`. An invalid timezone is rejected. Locale availability and application behavior vary. Inherited endpoint, proxy, and authentication variables are preserved; check `/status` for the actual authentication route. Shell hooks, settings files, plugins and background services may affect behavior. In particular, a previously running Claude Code background supervisor can have its own environment.

## 2. Claude Desktop for macOS

```sh
python3 tools/privacy.py app --timezone America/Los_Angeles --locale en_US.UTF-8
# If installed under a different name:
python3 tools/privacy.py app --app '/Applications/Claude.app'
```

This asks macOS Launch Services to open a new app instance with the specified environment values. Desktop may read OS preferences directly, reuse existing services, or use app-managed settings instead; these process overrides are an experiment, not a verified masking mechanism. Browser-based sign-in runs in its own browser process. Verify Desktop-specific behavior separately and use [official network settings](https://code.claude.com/docs/en/network-config) for network configuration.

## 3. Claude on the web

```sh
python3 tools/privacy.py web --browser chrome --timezone America/Los_Angeles --language en-US
# Or use Microsoft Edge:
python3 tools/privacy.py web --browser edge --timezone America/Los_Angeles --language en-US
```

The launcher creates a fresh, private browser data directory and opens `https://claude.ai/` in a separate profile. It prints that path locally. The profile can contain login cookies and other sensitive data; it is not deleted automatically. To reuse it, pass `--profile '/absolute/path/printed/earlier'`. Close the browser before manually deleting a profile you no longer need. Browser launches require the chosen browser to be installed.

Open `web/fingerprint.html` in that same browser profile and click **Inspect this browser**. It reports time zone, offset, languages, Intl locale, user agent, platform and a short list of approximate font-width probes. It has no network requests, analytics, WebRTC probes, IP lookup, or persistent storage. Browser, privacy settings, fallbacks and process reuse can change the result. The `--lang` flag is only a requested interface preference; browser `Accept-Language`, `navigator.languages`, and timezone behavior may differ. Verify the actual browser output before relying on it.

The browser launcher requests timezone/locale via Launch Services environment variables, but Chromium or macOS may obtain timezone from the OS or an existing service instead. The browser page is the verification mechanism; the launcher does not patch browser APIs or hide installed fonts. Browser extensions, WebRTC, server-side headers, account state, IP reputation and geolocation are outside this page's visibility.

## What these controls can and cannot do

| Surface | Controls | Verify | Important blind spots |
| --- | --- | --- | --- |
| CLI | Child-process timezone and locale | `audit` in the same environment; app-specific behavior separately | Existing background services, settings, server checks |
| Desktop | Launch Services environment request | App behavior separately | OS settings, app-managed services, browser sign-in |
| Web | Dedicated browser profile, language and environment requests | Open local inspector in that profile | Server headers, WebRTC, IP, fonts not covered, browser implementation |

These tools do not modify IP addresses, intercept traffic, bypass TLS, spoof account identity, or alter provider rules. A clean local inspection cannot establish access eligibility or account safety. Anthropic's [supported locations](https://support.claude.com/en/articles/8461763-where-can-i-access-claude), [data usage](https://code.claude.com/docs/en/data-usage), and [appeals](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) are the relevant official references.
