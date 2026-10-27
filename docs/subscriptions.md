# Subscription playbook

Last reviewed: October 27, 2026.

## Choose a billing route

Individual [Pro and Max subscriptions include Claude Code](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan). Check current limits and model availability before choosing. A higher tier should solve a demonstrated need; keep a short record of how often limits interrupt useful work.

Use the live [Pro overview](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan) and checkout for regional pricing, taxes, and monthly versus annual terms. This repository intentionally does not freeze a global price table.

According to the [billing FAQ](https://support.claude.com/en/articles/8325618-paid-plan-billing-faqs), web subscriptions accept credit or debit cards; app-store purchases are managed by that store. Store availability and payment eligibility require their own checks. An iOS purchase is a separate purchase channel, not a special macOS entitlement or a guarantee of regional access.

## Before checkout

- Verify current eligibility and your intended account.
- Check whether an active subscription already exists on the web or in an app store.
- Use accurate billing information and a payment method you are authorized to use.
- Review the amount, currency, taxes, renewal frequency, and cancellation route.
- Keep the receipt privately; do not share it with a reseller or public issue.

If a charge is declined, stop repeating attempts. Check the entered details privately, then ask your issuer or the billing provider for the actual failure reason. A decline alone does not prove an IP problem. Do not buy prepaid balances solely on a promise that they will make an ineligible subscription work.

## Keep a private subscription record

Store these fields in your own notes, outside this repository:

```text
Plan: Pro / Max / organization-provided
Purchase channel: Web / Apple / Google / employer
Next billing date: YYYY-MM-DD (confirm in provider UI)
Amount and currency: as displayed on invoice
Cancellation location: billing provider
Receipt location: private storage reference
Last review: YYYY-MM-DD
```

The record needs no card number, password, token, or full billing address. Review usage and any separately enabled extra charges before each renewal. A Claude subscription and Console/API billing are distinct; confirm your actual billing route with `/status` when using Code.

## Renewals, cancellation, and refunds

[Official cancellation instructions](https://support.claude.com/en/articles/8325617-cancel-your-pro-or-max-subscription) say to cancel at least 24 hours before the next billing date to avoid the next charge. Manage cancellation through the purchase platform; paid access normally continues to the end of the current period. Confirm the displayed end date and save the confirmation privately.

Use the local reminder tool three or more days ahead to leave time for review. Its date is an estimate you enter, not a live billing lookup. Refunds require a request to the relevant billing provider and are not guaranteed. For a locked account, use [official support](https://privacy.claude.com/en/articles/9015913-how-to-get-support) to ask about cancellation or refund eligibility.
