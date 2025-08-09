[backend]

- db for notifications sent to enforce notifications every 10-30min (as opposed to every 5s)
- limits on subscriptions per token (5)
- move from sqllite in memory db to production db
- ensure you cant unsubscribe someone else from their course

[mobile]

- integration
  - subscribedcourse component containing course name and trash bin icon beside it. these will be horizontally stacked with a max of 5. hitting the trash button will hit the unsubscribe api

[later]

- get notified if a course you're in got cancelled
