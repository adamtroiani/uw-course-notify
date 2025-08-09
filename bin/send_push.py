#!/usr/bin/env python3
import argparse, json, sys
import datetime as dt
from exponent_server_sdk import PushClient, PushMessage, PushServerError
from requests.exceptions import ConnectionError, HTTPError, Timeout


def main():
    ap = argparse.ArgumentParser(description="Send a test Expo push")
    ap.add_argument("token", help="Expo token, e.g. ExponentPushToken[xxxxxxxxxxxxxx]")
    ap.add_argument("--title")
    ap.add_argument("--body", default=str(dt.datetime.now()))
    args = ap.parse_args()

    token = args.token.strip()
    if not token.startswith("ExponentPushToken"):
        ap.error(
            "Token doesn’t look like an Expo push token (should start with 'ExponentPushToken')."
        )

    message = PushMessage(
        to=token, sound="default", title=args.title, body=args.body, priority="high"
    )

    client = PushClient()
    try:
        resp = client.publish(message)
    except PushServerError as exc:
        print(f"PushServerError: {exc}", file=sys.stderr)
        sys.exit(2)
    except (ConnectionError, HTTPError, Timeout) as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        sys.exit(3)

    # Pretty-print result
    try:
        data = resp["data"]
        if data.get("status") == "ok":
            print("✅ Sent OK. Ticket id:", data.get("id"))
        else:
            print("❌ Expo reported an error:", data)
    except Exception:
        print("Response:", resp)


if __name__ == "__main__":
    main()
