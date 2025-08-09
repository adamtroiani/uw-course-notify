I was inspired to build this app when I didn't get into CLAS 202. The course is extremely popular, and, because I'm busy at work, I probably wouldn't notice if a seat opened in the class. Moreover, I couldn't find a replacement course because nothing seemed interesting. If only there was a way I could have an edge over those that are manually checking UW Quest often to see if the course opened up...

There exists notification based solutions already - namely UWFlow - but it sends notifications via email and does not scrape the UWaterloo servers nearly as often. Having to remember check your emails often defeats the purpose, especially when the email might not be sent in time.

Enter UW Notify. A notification platform that will ping your phone within 5 seconds of a seat opening, giving you an edge over your peers in enrolling in a class when it becomes available, while removing the burden of manually checking Quest. Instead of having to check emails/Quest, the information you need comes to you.

There are two main components, the mobile app and the server.

1. Server - The server is deployed on an Oracle Cloud Always Free virtual machine. I built an API with FastAPI that can communicate with the mobile app. I also built a SQLite database using SQLAlchemy to keep track of the watchlist for each user (mobile device). The server polls the University of Waterloo Open Data API every 5 seconds, checking the availablility of only the courses that users desire to enroll in, and sends a push notification to each user when it sees an availability. The server uses Nginx to route requests through my personal domain, api.adamtroiani.com, using https for safer requests.

2. Mobile App - The mobile app is built with Expo + React Native as I wanted to reach iOS and Android users without doing double the work. The components in the app are how we interact with the API exposed by the server. For example, adding a course to our watchlist hits our "subscribe" API and removing a course hits the "unsubscribe" API.
