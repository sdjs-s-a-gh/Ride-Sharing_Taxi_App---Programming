This application was made as coursework for the Programming module that ran from February to May 2024. The code was last updated at 23/05/2024 at 3:27PM.

## Description
+ A full-stack web application developed using the Flask framework in Python – supporting user registration, driver profiles and ride creation.
+ Features responsive UI using HTML, Jinja and the Google Maps API to display real-time geolocation visualisations of user-generated ride routes. 
+ SQL queries to access and manipulate data from a local SQLite database, enabling user and driver information, settings, commenting and ride ratings to be managed.

## Features
Users may:
+ Select a driver
+ Book a journey from a specified location to a destination using the Google Maps API
+ Review a driver by rating them on a scale of one to five, and can also leaving a comment
+ Alter account details, including
  + username and password
  + primary and secondary colours of the website
  + notification preferences

Each driver in the system has their own unique profile -- detailing their name, car they are driving, aggregated review score and textual reviews. A hyperlink to show their current location is also provided.
