#!/usr/bin/env python3
"""
changelog-broadcast.py — K.x Closeout Slack/Teams Broadcast · I-NEW-16 · K.23

Reads /canonical/changelog.json (latest K.x entry by default) and posts a
formatted message to Slack OR Microsoft Teams via incoming webhook.

Webhook URL is read from (priority order):
  1. --webhook arg
  2. Environment variable: ANTS_BROADCAST_WEBHOOK
  3. Config file: scripts/.broadcast-webhook (one URL per line · gitignored)

Format auto-detected by URL substring:
  - hooks.slack.com         → Slack message format
  - .webhook.office.com     → Teams adaptive card

Owner: HoEng #21 + CCVO #52 (tone) + #63 FJA-CDCA Target #11

Usage:
  python3 changelog-broadcast.py                          # latest K.x · default webhook
  python3 changelog-broadcast.py --kref K.22              # specific K
  python3 changelog-broadcast.py --webhook https://...    # override webhook
  python3 changelog-broadcast.py --dry-run                # print payload only
  python3 changelog-broadcast.py --channel slack          # force format
  python3 changelog-broadcast.py --target teams           # force format
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CHANGELOG = WORKSPACE / "canonical" / "changelog.json"
WEBHOOK_FILE = WORKSPACE / "scripts" / ".broadcast-webhook"
HUB_INDEX_URL = "https://ai-solution-platform.github.io/AI-Hub/ANTS-2.0-Hub-Index.html"


def load_changelog():
    if not CHANGELOG.exists():
        print(f"❌ Changelog not found: {CHANGELOG}", file=sys.stderr)
        sys.exit(2)
    return json.loads(CHANGELOG.read_text(encoding="utf-8"))


def _kref_of(entry: dict) -> str:
    return entry.get("kx") or entry.get("k") or entry.get("kref") or entry.get("id", "K.?")


def _kref_sort_key(entry: dict):
    """Sort K.x entries · K.20.2 > K.20.1 > K.20 > K.19."""
    import re
    kref = _kref_of(entry)
    m = re.match(r"K\.(\d+)(?:\.(\d+))?", kref)
    if not m:
        return (0, 0)
    return (int(m.group(1)), int(m.group(2) or 0))


def get_latest_entry(changelog: dict, kref: str = None):
    entries = changelog.get("entries", []) or changelog.get("items", []) or []
    if not entries and isinstance(changelog, list):
        entries = changelog
    if not entries:
        for k in changelog:
            if isinstance(changelog[k], list):
                entries = changelog[k]
                break
    if not entries:
        print("❌ No K.x entries found in changelog", file=sys.stderr)
        sys.exit(2)
    if kref:
        for e in entries:
            if _kref_of(e) == kref:
                return e
        print(f"❌ K-ref '{kref}' not found in changelog", file=sys.stderr)
        sys.exit(2)
    # Pick the highest K.x.y by numeric sort
    return sorted(entries, key=_kref_sort_key, reverse=True)[0]


def _bullets_from(entry: dict):
    """Extract substantive bullets from various possible fields."""
    bullets = entry.get("bullets") or entry.get("items") or entry.get("deliverables")
    if not bullets:
        # Fall back to body_preview · split on bullet markers / line breaks
        body = entry.get("body_preview") or entry.get("body") or ""
        if body:
            import re
            # Pull lines starting with '- ' or '* ' or '• '
            lines = [ln.strip(" -*•·\t") for ln in re.split(r"[\n·]", body)
                     if ln.strip().startswith(("-", "*", "•")) or "ship" in ln.lower() or "ALL CLEAN" in ln]
            bullets = [ln for ln in lines if 10 < len(ln) < 200][:5]
    if isinstance(bullets, str):
        bullets = [bullets]
    return bullets or []


def resolve_webhook(arg_url: str = None) -> str:
    if arg_url:
        return arg_url
    env = os.environ.get("ANTS_BROADCAST_WEBHOOK")
    if env:
        return env
    if WEBHOOK_FILE.exists():
        for line in WEBHOOK_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                return line
    return None


def detect_target(webhook_url: str) -> str:
    if not webhook_url:
        return "unknown"
    if "hooks.slack.com" in webhook_url:
        return "slack"
    if "webhook.office.com" in webhook_url or "office365" in webhook_url:
        return "teams"
    return "generic"


def format_slack(entry: dict) -> dict:
    kref = _kref_of(entry)
    title = entry.get("title") or entry.get("summary", "K.x closeout")
    bullets = _bullets_from(entry)
    bullet_text = "\n".join(f"• {b}" for b in bullets[:6])
    status = entry.get("status", "")
    when = entry.get("date", "")

    return {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🚀 ANTS {kref} · {title[:120]}"},
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Date:*\n{when}"},
                    {"type": "mrkdwn", "text": f"*Status:*\n{status or '✅ Closed'}"},
                ],
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": bullet_text or "_(no deliverables listed)_"},
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Hub-Index"},
                        "url": HUB_INDEX_URL,
                    }
                ],
            },
        ]
    }


def format_teams(entry: dict) -> dict:
    kref = _kref_of(entry)
    title = entry.get("title") or entry.get("summary", "K.x closeout")
    bullets = _bullets_from(entry)
    facts = [
        {"name": "K-ref", "value": kref},
        {"name": "Date", "value": entry.get("date", "")},
        {"name": "Status", "value": entry.get("status", "✅ Closed")},
    ]
    return {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "themeColor": "0EA5A4",
        "summary": f"ANTS {kref} closeout",
        "title": f"ANTS {kref} · {title[:120]}",
        "sections": [
            {"facts": facts, "markdown": True},
            {"text": "  \n".join(f"• {b}" for b in bullets[:6]) or "_(no deliverables listed)_"},
        ],
        "potentialAction": [
            {
                "@type": "OpenUri",
                "name": "Hub-Index",
                "targets": [{"os": "default", "uri": HUB_INDEX_URL}],
            }
        ],
    }


def post(webhook_url: str, payload: dict, timeout: float = 10.0) -> int:
    import urllib.request
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook_url, data=body, method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except Exception as e:
        print(f"❌ Post failed: {e}", file=sys.stderr)
        return -1


def main():
    p = argparse.ArgumentParser(description="K.x Closeout Broadcast · I-NEW-16 · K.23")
    p.add_argument("--kref", help="Specific K-ref (default: latest)")
    p.add_argument("--webhook", help="Override webhook URL")
    p.add_argument("--target", choices=["slack", "teams", "auto"], default="auto")
    p.add_argument("--dry-run", action="store_true", help="Print payload, do not post")
    p.add_argument("--changelog", type=Path, default=CHANGELOG, help="Custom changelog path")
    args = p.parse_args()

    if args.changelog != CHANGELOG and not args.changelog.exists():
        print(f"❌ Changelog not found: {args.changelog}", file=sys.stderr)
        sys.exit(2)
    cl_path = args.changelog
    cl = json.loads(cl_path.read_text(encoding="utf-8")) if cl_path != CHANGELOG else load_changelog()

    entry = get_latest_entry(cl, kref=args.kref)
    webhook = resolve_webhook(args.webhook)
    target = args.target if args.target != "auto" else detect_target(webhook)

    if target == "teams":
        payload = format_teams(entry)
    else:
        payload = format_slack(entry)

    if args.dry_run or not webhook:
        if not webhook and not args.dry_run:
            print("⚠️  No webhook configured. Set --webhook · ANTS_BROADCAST_WEBHOOK env · or scripts/.broadcast-webhook file.")
            print("   Falling back to dry-run (printing payload):\n")
        print(f"=== Target: {target} ===")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(f"📡 Posting K.x closeout to {target} webhook...")
    status = post(webhook, payload)
    if 200 <= status < 300:
        print(f"✅ Broadcast posted · HTTP {status}")
    else:
        print(f"❌ Broadcast failed · HTTP {status}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
