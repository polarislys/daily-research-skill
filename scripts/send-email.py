#!/usr/bin/env python3
"""发送 daily research digest。支持 SMTP 或 Resend API。"""

from __future__ import annotations

import argparse
import os
import smtplib
import ssl
import sys
import urllib.error
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def send_smtp(
    to_addr: str,
    subject: str,
    text_body: str,
    html_body: str,
) -> None:
    host = env("SMTP_HOST")
    port = int(env("SMTP_PORT", "587"))
    user = env("SMTP_USER")
    password = env("SMTP_PASSWORD")
    from_addr = env("EMAIL_FROM", user)
    use_tls = env("SMTP_TLS", "true").lower() in ("1", "true", "yes")

    if not all([host, user, password, from_addr]):
        raise SystemExit("SMTP 模式需要 SMTP_HOST, SMTP_USER, SMTP_PASSWORD（可选 EMAIL_FROM）")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    if use_tls:
        with smtplib.SMTP(host, port, timeout=60) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(user, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
    else:
        with smtplib.SMTP_SSL(host, port, timeout=60) as server:
            server.login(user, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())


def send_resend(
    to_addr: str,
    subject: str,
    text_body: str,
    html_body: str,
) -> None:
    api_key = env("RESEND_API_KEY")
    from_addr = env("EMAIL_FROM")
    if not api_key or not from_addr:
        raise SystemExit("Resend 模式需要 RESEND_API_KEY 和 EMAIL_FROM")

    import json

    payload = json.dumps(
        {
            "from": from_addr,
            "to": [to_addr],
            "subject": subject,
            "text": text_body,
            "html": html_body,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status not in (200, 201):
                raise SystemExit(f"Resend 返回 {resp.status}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Resend 失败: {e.code} {body}") from e


def main() -> int:
    parser = argparse.ArgumentParser(description="Send daily research digest email")
    parser.add_argument("--digest-dir", type=Path, required=True, help="Directory with subject.txt, digest.txt, digest.html")
    parser.add_argument(
        "--provider",
        choices=["auto", "smtp", "resend"],
        default="auto",
        help="auto: RESEND_API_KEY 优先，否则 SMTP",
    )
    args = parser.parse_args()

    to_addr = env("EMAIL_TO")
    if not to_addr:
        raise SystemExit("需要环境变量 EMAIL_TO")

    subject = (args.digest_dir / "subject.txt").read_text(encoding="utf-8").strip()
    text_body = (args.digest_dir / "digest.txt").read_text(encoding="utf-8")
    html_body = (args.digest_dir / "digest.html").read_text(encoding="utf-8")

    provider = args.provider
    if provider == "auto":
        provider = "resend" if env("RESEND_API_KEY") else "smtp"

    if provider == "resend":
        send_resend(to_addr, subject, text_body, html_body)
    else:
        send_smtp(to_addr, subject, text_body, html_body)

    print(f"Sent to {to_addr} via {provider}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
