# AI Electricity Bill Analyzer

An AI-powered electricity bill reading and management system built with Flask, PyMongo, EasyOCR, and HTML/CSS/JS.

## Database: MongoDB Atlas

This project uses **MongoDB Atlas** for database management.

### Setup Instructions

1. **Configure Environment Variables**:
   Open `backend/.env` (or copy `backend/.env.example` to `backend/.env`) and set your MongoDB Atlas URI:
   ```env
   MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/electric_ai?retryWrites=true&w=majority
   DATABASE_NAME=electric_ai
   SECRET_KEY=electric_ai_project
   ```

2. **MongoDB Atlas Requirements**:
   - Ensure you have created a database user under **Database Access** in MongoDB Atlas.
   - Add your IP address (or `0.0.0.0/0`) under **Network Access** in MongoDB Atlas.

3. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Run the Project**:
   Double click `start_project.bat` or run manually:
   - Backend: `python backend/app.py`
   - Frontend: `python -m http.server 5500 --bind 127.0.0.1` (from `frontend/` directory)
