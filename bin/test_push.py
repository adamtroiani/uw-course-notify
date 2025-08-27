from exponent_server_sdk import PushClient, PushMessage, PushServerError

push = PushClient()

def test_push(token):
  try:
    ticket = push.publish(PushMessage(
      to=token,
      title="UW Notify test",
      body="Hello from server",
      sound="default",
      channel_id="default",   # harmless on iOS
      priority="high"
    ))
    receipts = push.check_receipts([ticket])
    print("TOKEN:", token)
    print("TICKET:", ticket)
    print("RECEIPTS:", receipts)
  except PushServerError as e:
    print("PUSH ERROR:", e.response.json())

# Test both:
test_push("ExponentPushToken[GBpRR1IJ39MhTdHE5ZU2H_]")
test_push("ExponentPushToken[sA7z8-BDdnS1ZQkvzHXg82]")
