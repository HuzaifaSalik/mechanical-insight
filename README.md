# Company Insight - Engineering & Simulation Services Website

A professional Flask-based website for **Company Insight**, showcasing engineering and simulation services with a bold, modern design featuring interactive animations and comprehensive service management.

## Features

- Modern, responsive design with Tailwind CSS
- Interactive animations using GSAP and AOS
- Service showcase with detailed pages
- Portfolio/case studies section
- Blog system with categories and search
- Contact form with email notifications
- Admin panel for content management
- SQLite database (development) / PostgreSQL (production)
- SEO-optimized with meta tags and sitemap

## Services Offered

1. Product Design & CAD Modeling
2. Mechanical Design & Structural Analysis (FEA)
3. Automotive & Transportation Simulations
4. Aerospace & UAV Engineering Support
5. Manufacturing & Industrial Equipment Analysis
6. Computational Fluid Dynamics (CFD) Simulations
7. Thermal & Heat Transfer Analysis

## Tech Stack

### Backend
- Flask 3.0
- SQLAlchemy (ORM)
- Flask-Migrate (Database migrations)
- Flask-WTF (Forms)
- Flask-Mail (Email)
- Flask-Login (Authentication)
- Flask-Admin (Admin panel)
- Flask-Limiter (Rate limiting)

### Frontend
- Tailwind CSS 3.4+
- GSAP (Animation library)
- AOS (Animate On Scroll)
- Alpine.js (Lightweight interactivity)
- Font Awesome 6 (Icons)
- Google Fonts (Typography)

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   cd "c:\New folder"
   ```

2. **Activate the virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies** (Already completed if you see this)
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env` file and update with your settings:
     - `SECRET_KEY`: Generate a secure random key
     - `MAIL_USERNAME`: Your Gmail address
     - `MAIL_PASSWORD`: Gmail app password (not your regular password)
     - `RECAPTCHA_PUBLIC_KEY` and `RECAPTCHA_PRIVATE_KEY`: Get from Google reCAPTCHA

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Seed the database with services**
   ```bash
   python run.py seed_services
   ```

7. **Create an admin user**
   ```bash
   python run.py create_admin
   ```
   Follow the prompts to create your admin account.

8. **Run the development server**
   ```bash
   python run.py
   ```
   or
   ```bash
   flask run
   ```

9. **Access the website**
   - Website: http://localhost:5000
   - Admin panel: http://localhost:5000/admin/login

## Project Structure

```
c:\New folder\
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models
│   ├── config.py                # Configuration classes
│   ├── main/                    # Main blueprint (public pages)
│   │   ├── routes.py            # Routes for home, services, contact
│   │   └── forms.py             # Contact form
│   ├── blog/                    # Blog blueprint
│   │   └── routes.py
│   ├── portfolio/               # Portfolio blueprint
│   │   └── routes.py
│   ├── admin/                   # Admin blueprint
│   │   └── routes.py
│   ├── templates/               # HTML templates
│   │   ├── base.html
│   │   ├── components/          # Reusable components
│   │   │   ├── navbar.html
│   │   │   └── footer.html
│   │   ├── main/
│   │   │   ├── index.html
│   │   │   └── contact.html
│   │   └── errors/
│   └── static/                  # Static files
│       ├── css/
│       │   ├── main.css
│       │   └── animations.css
│       ├── js/
│       │   ├── main.js
│       │   ├── animations.js
│       │   └── contact.js
│       └── images/
├── venv/                        # Virtual environment
├── .env                         # Environment variables
├── .gitignore
├── config.py                    # Configuration loader
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

## Database Models

### Service
- Engineering services with descriptions, icons, and SEO metadata
- Fields: title, slug, subtitle, description, icon_class, features, order, is_active

### CaseStudy
- Portfolio projects with challenge/solution/results structure
- Fields: title, slug, client, industry, challenge, solution, results, images, technologies

### BlogPost
- Blog articles with categories, tags, and view counter
- Fields: title, slug, subtitle, content, category, tags, featured, views, is_published

### ContactSubmission
- Contact form submissions with status tracking
- Fields: name, email, company, phone, service_interest, message, status, notes

### User
- Admin users for authentication
- Fields: username, email, password_hash, is_admin

## Configuration

### Environment Variables (.env)

```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///companyinsight.db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@companyinsight.com

# Admin Credentials
ADMIN_EMAIL=admin@companyinsight.com
ADMIN_PASSWORD=admin123

# Google reCAPTCHA (Optional)
RECAPTCHA_PUBLIC_KEY=your-site-key
RECAPTCHA_PRIVATE_KEY=your-secret-key
```

### Gmail App Password Setup

1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Authentication
3. Go to App Passwords
4. Generate a new app password for "Mail"
5. Use this password in `MAIL_PASSWORD`

## Usage

### Adding Services
Services are pre-seeded using the `seed_services` command. To add more:
1. Access the admin panel at `/admin`
2. Navigate to Services
3. Click "Create" and fill in the details

### Managing Portfolio
1. Log in to admin panel
2. Navigate to Case Studies
3. Add new projects with images and descriptions

### Creating Blog Posts
1. Access admin panel
2. Navigate to Blog Posts
3. Create new posts with rich text editor

### Viewing Contact Submissions
1. Log in to admin panel
2. Navigate to Contact Submissions
3. View and manage inquiries

## Deployment

### Heroku

1. **Create Heroku app**
   ```bash
   heroku create company-insight
   ```

2. **Add Heroku Postgres**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

3. **Set environment variables**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-production-secret
   heroku config:set MAIL_USERNAME=your-email@gmail.com
   heroku config:set MAIL_PASSWORD=your-app-password
   ```

4. **Deploy**
   ```bash
   git push heroku master
   ```

5. **Initialize database**
   ```bash
   heroku run flask db upgrade
   heroku run python run.py seed_services
   heroku run python run.py create_admin
   ```

### DigitalOcean / VPS

1. Install dependencies on server
2. Configure Nginx as reverse proxy
3. Use Gunicorn as WSGI server
4. Set up SSL with Let's Encrypt
5. Configure systemd for process management

## Design System

### Colors
- **Electric Blue**: #0066FF (Primary brand color)
- **Deep Navy**: #0A1628 (Dark backgrounds)
- **Vibrant Cyan**: #00D9FF (Accents)
- **Neon Green**: #00FF88 (CTAs, success states)
- **Bright Orange**: #FF6B35 (Energy, urgency)
- **Purple**: #8B5CF6 (Creativity, premium)

### Typography
- **Headings**: Space Grotesk (Bold, modern)
- **Body**: Inter (Readable, professional)
- **Monospace**: JetBrains Mono (Technical specs)

### Animations
- GSAP for complex hero animations
- AOS for scroll-triggered effects
- Hover effects: scale, glow, lift
- Number counters for statistics
- Parallax backgrounds

## API Endpoints

### Public Routes
- `/` - Homepage
- `/about` - About page
- `/services` - Services overview
- `/services/<slug>` - Individual service page
- `/portfolio` - Portfolio listing
- `/portfolio/<slug>` - Case study detail
- `/blog` - Blog listing
- `/blog/<slug>` - Blog post
- `/contact` - Contact form

### Admin Routes (Login Required)
- `/admin/login` - Admin login
- `/admin/dashboard` - Admin dashboard
- `/admin/contacts` - Contact submissions
- `/admin` - Flask-Admin interface

## Testing

Run tests (when test suite is created):
```bash
pytest
pytest --cov=app
```

## Troubleshooting

### Database Issues
```bash
# Reset database
rm companyinsight.db
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python run.py seed_services
```

### Email Not Sending
- Check Gmail app password is correct
- Ensure 2FA is enabled on Gmail account
- Verify `MAIL_USE_TLS=True` in .env
- Check firewall/antivirus blocking port 587

### Static Files Not Loading
- Clear browser cache
- Check file paths are correct
- Ensure static folder is in correct location
- Verify Flask is serving static files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is proprietary and confidential.

## Support

For support, email info@companyinsight.com or visit our contact page.

## Credits

Built with Flask, Tailwind CSS, GSAP, and AOS.
Designed and developed for Company Insight.

---

Last updated: January 2026
