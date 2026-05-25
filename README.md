# Crocodile Analytics 

## Project Overview

Crocodile Analytics is a football web application developed with Flask and MySQL for a university project. The system allows admins to manage football data while users can view players, teams, matches, statistics, and news.

---

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS

---

## Features

### Admin Features
- Manage players
- Manage teams
- Manage matches
- Add news posts
- View statistics
- API information page

### User Features
- View players
- View teams
- View statistics
- Read latest news

---

## Database Tables

- users
- players
- teams
- matches
- news

---

## Project Structure

```text
cmp210-project-main/
│
├── app.py
├── requirements.txt
│
├── statics/
│   ├── style.css
│   └── images/
│       ├── Artboard 1.png
│       ├── download.webp
│       └── PSG Neymar.jpg
│
├── templates/
│   ├── base.html
│   ├── login.html
│   │
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── players.html
│   │   ├── teams.html
│   │   ├── matches.html
│   │   ├── statistics.html
│   │   ├── news.html
│   │   ├── api_info.html
│   │   ├── add_player.html
│   │   ├── edit_player.html
│   │   ├── add_team.html
│   │   ├── edit_team.html
│   │   ├── add_match.html
│   │   └── edit_match.html
│   │
│   └── user/
│       ├── dashboard.html
│       ├── players.html
│       ├── teams.html
│       └── statistics.html
```

---

## Challenges

Some challenges during development included:

- Organizing Flask routes
- Connecting Flask with MySQL
- Creating CRUD operations
- Designing the UI

---

## Future Improvements

- Live football API integration
- Better statistics
- Mobile optimization
- Team logos and images

---

## Conclusion

This project helped us improve understanding of Flask, MySQL, authentication systems, and web application development while creating a simple football analytics platform.



