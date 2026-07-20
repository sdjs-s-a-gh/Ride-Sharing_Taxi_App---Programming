<div align="center">
  <h1>Ride-Sharing Taxi Application</h1>
</div>

The __Ride-Sharing Taxi Application__ is a full-stack website built using the Python framework Flask. The website was developed to allow users to schedule taxi rides from a pre-determined location and destination, while uniquely being able to discount their fee by sharing the ride with a friend or random user.

The Taxi application offers functionality for users to view the real-time location of available drivers, their profile, book rides with others using a search feature and leave driver ratings alongside a textual review. Additional support for customising user profiles is provided, allowing changes to the user interface, notification preferences and account information.

---
## Background
This project was made as coursework for the "Programming" module that ran from February to May 2024. The code was last updated at 23th May 2024 at 3:27PM.

---
## Key Features
1. Driver Discovery: Users may browse a registry of current drivers either in a menu format, view their profile and past reviews, see real-time locations on a map and book journeys.
2. Ride Lifecycle: Users can book journeys from a specific collection point to destination, receive a predicted price, visualise the route and complete the ride.
3. Reviews: Once a journey has been completed, users can rate the driver on a scale from 1 to 5 with an accompanied, but optional, textual review. These reviews are appended to a driver's profile and can be viewed by other users.
4. Personalisation: The application offers a plethora of customisation offers that users may utilise, including user interface colour schemes, notification preferences and account information like usernames and emails.

---
## Technology Stack
<table>
  <tr>
    <th>Layer</th>
    <th>Technology</th>
    <th>Role</th>
  </tr>
  <tr>
    <td>Frontend</td>
    <td>HTML5, CSS3 and Jinja2</td>
    <td>User Interface and styling</td>
   <tr>
    <td>Geospatial Mapping</td>
    <td>Google Maps API</td>
    <td>Geospatial visualisation of routes and real-time driver location</td>
  </tr>
  <tr>
    <td>Backend</td>
    <td>Flask (Python 3.12)</td>
    <td>Routing and user session management</td>
  </tr>
    <tr>
    <td>Database</td>
    <td>SQLite</td>
    <td>Persistent storage for users, drivers, rides and user settings</td>
  </tr>
</table>
