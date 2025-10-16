# Sonship Bible Study Platform

A beautiful, Bible.com-inspired Bible study platform with comprehensive sonship theology commentary on every verse.

![Sonship Bible](https://img.shields.io/badge/verses-7543-green) ![Commentary](https://img.shields.io/badge/commentary-100%25-gold) ![Status](https://img.shields.io/badge/status-live-success)

## 🌟 Features

- **7,543 verses** with 100% sonship theology commentary
- **Bible.com-inspired design** - Clean, minimal, professional
- **Sonship Insights** - Every verse includes theological commentary focused on adoption, identity, and relationship with the Father
- **Mobile-responsive** - Works beautifully on all devices
- **Fast & lightweight** - Vanilla JavaScript, no heavy frameworks
- **Copy & share** - Easy verse sharing functionality
- **Smart navigation** - Automatic chapter detection and smooth transitions

## 📖 About Sonship Theology

This platform provides verse-by-verse commentary emphasizing:
- **Adoption** as sons and daughters of God
- **Identity** in Christ as beloved children
- **Intimacy** with our Abba Father
- **Inheritance** and freedom in the Spirit
- **Relationship** over religion

## 🚀 Live Demo

**Visit:** [https://study.sonship.ai](https://study.sonship.ai)

## 🛠️ Technology Stack

- **Backend:** Flask (Python 3.12)
- **Database:** PostgreSQL 15
- **Server:** Gunicorn
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Design:** Bible.com-inspired minimal UI

## 📦 Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/mikee-ai/sonship-bible-study.git
cd sonship-bible-study
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Set up database**
```bash
# Create PostgreSQL database
createdb sonship_db

# Import the database schema and data (provided separately)
psql -U postgres -d sonship_db -f database/schema.sql
psql -U postgres -d sonship_db -f database/data.sql
```

6. **Run the application**
```bash
# Development
python app.py

# Production
gunicorn --workers 3 --bind 0.0.0.0:5001 app:app
```

## 🎨 Design Philosophy

### Bible.com-Inspired
- Clean white background
- Generous whitespace
- Professional typography
- Subtle interactions
- Accessible color palette
- Mobile-first responsive design

### Color Palette
```css
--primary: #2e7d32        /* Green for primary actions */
--bg-white: #ffffff       /* Main background */
--bg-gray: #f5f5f5        /* Secondary background */
--text-primary: #212121   /* Main text */
--text-secondary: #757575 /* Secondary text */
--accent-gold: #ffa726    /* Sonship Insight boxes */
```

## 📱 API Endpoints

### Get Books
```
GET /api/books
```
Returns list of all books with verse counts and commentary statistics.

### Get Chapter
```
GET /api/chapter/<book>/<chapter>
```
Returns all verses and commentary for a specific chapter.

### Search (Coming Soon)
```
GET /api/search?q=<query>
```
Full-text search across verses and commentary.

## 🗄️ Database Schema

### Verses Table
```sql
CREATE TABLE verses (
    id SERIAL PRIMARY KEY,
    book VARCHAR(10) NOT NULL,
    chapter INTEGER NOT NULL,
    verse_number INTEGER NOT NULL,
    verse_text TEXT NOT NULL,
    insight TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎯 Roadmap

### Short-term
- [ ] Add search functionality
- [ ] Complete Matthew chapters 1-12
- [ ] Add Old Testament books
- [ ] User accounts and favorites

### Long-term
- [ ] Reading plans
- [ ] Audio Bible integration
- [ ] Mobile apps (iOS/Android)
- [ ] Community features
- [ ] Multiple Bible translations
- [ ] Personal highlighting and notes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bible.com** for design inspiration
- **Sonship theology** teachers and authors
- **Open-source community** for amazing tools

## 📧 Contact

**Website:** [https://study.sonship.ai](https://study.sonship.ai)

## ⭐ Support

If you find this project helpful, please consider giving it a star on GitHub!

---

**Built with ❤️ for the body of Christ**

