PRIVACY_HTML = """
<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Privacy Policy — UW Notify</title>
<style> body{font:16px/1.6 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;padding:2rem;max-width:800px;margin:0 auto;color:#111}
h1{font-size:28px;margin:0 0 1rem} h2{font-size:18px;margin:1.5rem 0 .5rem}
small{color:#666} ul{margin:.3rem 0 .8rem 1.2rem} </style>
</head><body>
<h1>Privacy Policy — UW Notify</h1>
<small>Last updated: 26 Aug 2025</small>
<p>UW Notify helps University of Waterloo students track course availability and receive notifications.</p>
<h2>Data We Collect</h2>
<ul>
  <li><b>Expo push token</b> (device identifier) to send notifications</li>
  <li><b>Watchlist items</b> you add (course codes & terms)</li>
  <li><b>Diagnostics</b> (basic logs/crash reports) from the platform/providers</li>
</ul>
<p>We do not collect names, emails, or precise location.</p>
<h2>How We Use Data</h2>
<ul>
  <li>To deliver push notifications about your watchlist</li>
  <li>To maintain and improve reliability and security</li>
</ul>
<h2>Sharing</h2>
<p>We do not sell your data. We share only with service providers that enable core features (e.g., Expo Push Service, hosting) under appropriate safeguards.</p>
<h2>Retention & Deletion</h2>
<ul>
  <li>Watchlist + push token are kept while notifications are enabled</li>
  <li>Remove courses or uninstall the app to stop notifications</li>
  <li>To request deletion of server-stored data, email <a href="mailto:dev@adamtroiani.com">dev@adamtroiani.com</a> and include your device’s push token from the app</li>
</ul>
<h2>Contact</h2>
<p>Adam Troiani — <a href="mailto:dev@adamtroiani.com">dev@adamtroiani.com</a></p>
</body></html>
"""

SUPPORT_HTML = """
<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Support — UW Notify</title>
<style>
  body{font:16px/1.6 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;padding:2rem;max-width:800px;margin:0 auto;color:#111}
  h1{font-size:28px;margin:0 0 1rem}
  h2{font-size:18px;margin:1.5rem 0 .5rem}
  small{color:#666}
  ul{margin:.3rem 0 .8rem 1.2rem}
  code{background:#f6f6f6;padding:.1rem .3rem;border-radius:4px}
  a{color:#0b63ff;text-decoration:none}
  a:hover{text-decoration:underline}
</style>
</head><body>
<h1>Support — UW Notify</h1>
<small>Last updated: 26 Aug 2025</small>

<p>Welcome! This page explains how to get help with UW Notify and includes quick troubleshooting tips.</p>

<h2>Contact</h2>
<p>Email: <a href="mailto:dev@adamtroiani.com">dev@adamtroiani.com</a></p>
<ul>
  <li>Please include your device model (e.g., iPhone 14), OS version (e.g., iOS 17.x / Android 14), app version (see App Store / Play Store), and a short description of the issue.</li>
  <li>Screenshots are helpful when possible.</li>
</ul>

<h2>Quick Troubleshooting</h2>
<ul>
  <li><b>Not receiving notifications (iOS):</b> In <i>Settings → Notifications → UW Notify</i>, enable <b>Allow Notifications</b> and <b>Banners</b>. Ensure Focus/Do Not Disturb is off. Open the app once to refresh your notification token.</li>
  <li><b>Not receiving notifications (Android):</b> Ensure notifications are allowed, disable battery optimizations for UW Notify if available, and open the app to refresh the token.</li>
  <li><b>Foreground alerts:</b> If the app is open and you don’t see banners, check your device notification settings; foreground presentation depends on system settings.</li>
  <li><b>Adding a course fails:</b> Use the format <code>SUBJ 123</code> (e.g., <code>CLAS 202</code>) and choose the correct term. Check your internet connection and try again.</li>
  <li><b>Update the app:</b> Install the latest version from the App Store / Google Play and try again.</li>
</ul>

<h2>Request Data Deletion</h2>
<p>UW Notify stores your watchlist and an Expo push token to deliver notifications. To request deletion of this data, email
<a href="mailto:dev@adamtroiani.com">dev@adamtroiani.com</a>. If possible, include your device’s push token (you can copy it from the app if exposed, or request instructions).</p>

<h2>Report a Bug</h2>
<ul>
  <li>Steps to reproduce (what you tapped/entered)</li>
  <li>Course code & term (if relevant)</li>
  <li>Device, OS version, and app version</li>
  <li>Screenshots or screen recording (optional)</li>
</ul>

<h2>Links</h2>
<ul>
  <li><a href="/privacy">Privacy Policy</a></li>
</ul>

<p>Thank you for using UW Notify!</p>
</body></html>
"""