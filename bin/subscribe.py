import argparse, json, signal, sys, time
from typing import Optional
import requests

API_URL = "https://api.adamtroiani.com"
TOKEN = "ExponentPushToken[24YVlOOpbEHj6RqLAT2EAM]"
TIMEOUT = 5


def post_json(url: str, payload: dict) -> dict:
    r = requests.post(url, json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    try:
        return r.json()
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser(
        description="Subscribe to a course via the UW-Notify API; unsubscribes on Ctrl+C."
    )
    ap.add_argument("course", help='Course code, e.g. "CLAS 202"')
    ap.add_argument("term", type=int, help="Term code, e.g. 1259")

    args = ap.parse_args()

    sub = {
        "course": args.course.strip(),
        "term": args.term,
        "push_token": TOKEN,
    }

    subscribe_url = API_URL + "/subscribe"
    unsubscribe_url = API_URL + "/unsubscribe"

    subscribed = False
    unsubscribed = False

    def cleanup(signum: Optional[int] = None, frame=None):
        nonlocal unsubscribed
        if not subscribed or unsubscribed:
            sys.exit(0)
        try:
            resp = post_json(unsubscribe_url, sub)
            deleted = resp.get("deleted")
            print(f"\nUnsubscribe -> deleted={deleted}")
        except Exception as e:
            print(f"\nUnsubscribe failed: {e}", file=sys.stderr)
        finally:
            unsubscribed = True
            sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)  # Ctrl+C

    try:
        resp = post_json(subscribe_url, sub)
        created = resp.get("created")
        print(f"Subscribe -> created={created}")
        subscribed = True
    except Exception as e:
        print(f"Subscribe failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("Subscribed. Press Ctrl+C to unsubscribe and exit…")
    try:
        while input() != "q":
            pass
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
