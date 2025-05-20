# Research Collaboration Portal

The Research Collaboration Portal is a web application designed to connect researchers by facilitating idea sharing, discussions, and collaboration. The portal offers various features such as creating profiles, posting research ideas, and interacting with other users' content. It aims to simplify the process of finding Research Assistant (RA) opportunities for college students, reducing the need for cold emails to professors, which can often be inconvenient for both students and faculty.

---

## Features

### 1. User Authentication
- **Sign Up**: Create a new account.
- **Login/Logout**: Secure access to the portal.
- **Session Management**: Prevents unauthorized access to restricted pages after logout.

### 2. Forum Page
- **Post Ideas**: Share your research ideas and projects.
- **Comment Section**: Leave feedback or thoughts on specific posts.
- **Discussion Threads**: Encourage collaborative discussions.

### 3. Profile Management
- **View Profiles**: Explore other researchers' profiles.
- **Search Filter**: Filter profiles based on specific criteria.

### 4. Search and Filter
- **Search Bar**: Filter research ideas and profiles easily.
- **Profile Filter**: Find researchers with similar interests or skills.

---

## Set-Up Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- Flask
- Flask-Login
- SQLAlchemy

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kmdikshitha/CollabHub.git
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   - Initialize the database:
     ```bash
     flask db init
     flask db migrate -m "Initial migration"
     flask db upgrade
     ```
   - This will create the necessary tables in your database.

5. **Run the Application**:
   ```bash
   flask run
   ```
   - The application will be available at `http://127.0.0.1:5000/`.

6. **(Optional) Set Up Environment Variables**:
   - Create a `.env` file in the root directory and include:
     ```env
     FLASK_APP=run.py
     FLASK_ENV=development
     SECRET_KEY=your_secret_key_here
     DATABASE_URL=sqlite:///your_database_name.db
     ```

---

## Additional Resources

- [Idea Proposal Presentation](https://docs.google.com/presentation/d/1-Dcvp69AX49po2Vs9qhSzBYI-PbhT1Ha/edit?usp=sharing&ouid=101473124620224721303&rtpof=true&sd=true)

---

## Future Enhancements
- Real-time notifications for new comments or posts.
- Integration with academic publication databases (e.g., PubMed, IEEE Xplore).
- Advanced analytics and insights for researchers.
- Multi-language support.

