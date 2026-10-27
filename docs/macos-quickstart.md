# macOS quickstart

Last reviewed: October 27, 2026. Source: [official installation guide](https://code.claude.com/docs/en/setup).

## Prepare

Confirm eligibility first. The official setup page currently lists macOS 13+ and 4 GB+ RAM, with Intel and Apple Silicon support. Keep your operating system updated. Save your project in a folder you control.

## Install

If you already use Homebrew:

```sh
brew install --cask claude-code
claude --version
claude doctor
```

The official setup page also provides a native installer. Read that page directly before executing its download command. Choose one installation method to make updates easier to understand. Homebrew installations can be updated with `brew upgrade claude-code`.

If a native installation is missing from your PATH, consult the official troubleshooting documentation before changing shell files. Do not use `sudo` to repair a user installation blindly.

## Sign in and verify

Open Terminal in your project directory and run `claude`. Complete the browser sign-in with the account that owns the subscription. In the interactive session, use `/login` to change accounts and `/status` to inspect the active authentication method.

An approved `ANTHROPIC_API_KEY` can select API billing even when you have a subscription. For a subscription session, remove it from the current shell:

```sh
unset ANTHROPIC_API_KEY
claude
```

Then check `/status` again. If it returns after opening a new terminal, review your shell startup files or environment manager locally. Do not paste their contents into a public issue. See [official authentication guidance](https://support.claude.com/en/articles/12304248-manage-api-key-environment-variables-in-claude-code).

## First session

Start with a small request such as explaining a function. Review proposed edits and permissions before granting them. Commit your work regularly. Use the account's available model selector rather than assuming every plan always includes every new model.

For a graphical workflow, follow the Desktop link from the official setup page. Terminal environment variables and graphical app settings can differ; see the network guide.
