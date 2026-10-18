# 📚 Learning Log

> **A personal knowledge management web application for students and self-learners.**
> Organize your study materials by topics, write formatted notes with Markdown, and revisit what matters most with the **Favorites** feature.
> Perfect for active learning, spaced repetition, and building your own digital second brain.

---

## ✨ Features

- **🗂️ Topic-based organization** — Group notes under custom topics (e.g., "Python", "Calculus", "Django").
- **📝 Markdown support** — Write richly formatted notes with bold, italics, code blocks, lists, and links.
- **👁️ Live preview** — See how your note will look while editing, without leaving the form.
- **🔍 Search & sort** — Instantly find topics or entries; sort by date (newest/oldest) or alphabetically.
- **🖍️ Highlight on search** — Matched words are highlighted in entries for quick navigation.
- **⭐ Favorites (Bookmarks)** — Star important topics or entries for quick review.
- **💾 Export & import** — Backup or share your knowledge as JSON files.
- **😊 Emoji picker** — Insert emojis directly into your notes.
- **🌙 Dark / Light mode** — Switch themes with one click, saved across sessions.
- **📱 Responsive design** — Works great on desktops, tablets, and phones.

---

## 🖼️ Screenshots

| Light Theme | Dark Theme | Favorites |
|:-----------:|:----------:|:---------:|
| ![Light Theme](docs/screenshot-topics-light.png) | ![Dark Theme](docs/screenshot-topics-dark.png) | ![Favorites](docs/screenshot-favourites.png) |

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python, Django |
| **Frontend** | HTML5, CSS3, Bootstrap 4, Vanilla JavaScript |
| **Database** | SQLite (development), PostgreSQL-ready |
| **Libraries** | `markdown`, `django-bootstrap4`, `marked` (JS) |
| **Deployment** | Ready for Heroku, Render, Railway, or any WSGI server |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/learning-log.git
cd learning-log
```

### 2. Set up a virtual environment
```
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run migrations and create a superuser
```
python manage.py migrate
python manage.py createsuperuser
```

### 5. Start the development server
```
python manage.py runserver
```

### 6. Open in browser
Navigate to http://127.0.0.1:8000

---

## 📁 Project Structure
learning_log/
├── learning_logs/          # Core app
│   ├── models.py           # Topic, Entry, Bookmark
│   ├── views.py            # Request handlers
│   ├── urls.py             # Routing
│   ├── forms.py            # Django forms
│   └── templatetags/       # Custom filters (markdownify, rough_timesince)
├── users/                  # Authentication (login, register, logout)
├── templates/              # Base and page HTML templates
├── static/                 # CSS, JS, images
── docs/                   # Screenshots for README
── manage.py               # Django management script
└── requirements.txt        # Python dependencies

---

## 📖 Usage
### Creating a topic
1. Click + Add new topic on the Topics page.
2. Enter a name (e.g., "Machine Learning") and save.
### Writing an entry
1. Open a topic.
2. Click + Add new entry.
3. Write your note using Markdown syntax.
4. Use the Preview button to see the rendered result.
5. Click Add entry to save.
### Searching and sorting
- Use the search field to filter topics or entries by keyword.
- Use the Sort dropdown to order by date or alphabetically.
### Using Favorites
- Click the ★ icon next to any topic or entry to add it to Favorites.
- Access all starred items from the Bookmarks tab in the navbar.
### Exporting / Importing
- On a topic page, click Export topic to download a .json backup.
- On the "Add new topic" page, use Import topic to restore from a file.

---

## 🤝 Contributing
1. Contributions, issues, and feature requests are welcome!
2. Fork the repository.
3. Create your feature branch: git checkout -b feature/AmazingFeature
4. Commit your changes: git commit -m 'Add some AmazingFeature'
5. Push to the branch: git push origin feature/AmazingFeature
6. Open a Pull Request.

---

## License
This project is open-source and available under the MIT License.
---

## Acknowledgements
- 📖 Inspired by Python Crash Course by Eric Matthes
- 🎨 UI built with Bootstrap 4
- 📝 Markdown parsing powered by the Python-Markdown library
- 👁️ Live preview uses marked.js
