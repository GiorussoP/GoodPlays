# 🚀 GoodPlays Frontend - Quick Start Guide

## Setup & Installation

### 1. Prerequisites
- Python 3.8+
- pip or conda
- Modern web browser (Chrome, Firefox, Safari, Edge)

### 2. Install Backend & Dependencies
```bash
# Navigate to project directory
cd /home/victor/Projects/graduacao/GoodPlays

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Server
```bash
uvicorn app.main:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### 4. Open in Browser
Navigate to: **http://localhost:8000**

---

## 🎯 First-Time User Flow

### Step 1: Register a New Account
1. Click **"Join Now"** on home page (or go to `/register`)
2. Enter:
   - **Username:** mycoolname (3+ characters)
   - **Email:** me@example.com
   - **Password:** mypassword (6+ characters)
   - **Confirm Password:** mypassword
3. Click **"Create Account"**
4. You'll be redirected to login page

### Step 2: Login
1. Enter your username and password
2. Click **"Sign In"**
3. You'll be redirected to Games page

### Step 3: Browse Games
1. You're now on the **Games** page (`/games`)
2. Use the **search box** to find games by title
3. Use the **genre dropdown** to filter
4. Click **"View Details"** on any game card

### Step 4: Add a Game (Optional)
If you want to add a new game to the platform:
1. Click **"Add New Game"** button
2. Fill in:
   - Title (required)
   - Description
   - Developer
   - Genre
   - Release Year
3. Click **"Add Game"**

### Step 5: View Game Details
On a game detail page, you can:

**Track Progress:**
- Click **"Start Playing"** or **"Update Progress"**
- Set completion percentage (0-100%)
- Set last played date/time
- Click **"Save Progress"**

**Write a Review:**
- Click **"Write a Review"**
- Select star rating (1-5 stars)
- Add optional comment
- Click **"Post Review"**

**Read Reviews:**
- Scroll down to see all community reviews
- View ratings and comments from other players

### Step 6: View Your Profile
1. Click **"Profile"** in navigation (top right)
2. See your statistics:
   - Games in progress count
   - Reviews written count
3. View all games you're tracking
4. See all reviews you've written

---

## 📱 Navigation Guide

| Page | URL | Access | Purpose |
|------|-----|--------|---------|
| Home | `/` | Everyone | Overview & featured games |
| Login | `/login` | Everyone | Sign in to account |
| Register | `/register` | Everyone | Create new account |
| Games | `/games` | Everyone | Browse all games |
| Game Detail | `/game/{id}` | Everyone | View game & reviews |
| Profile | `/profile` | Logged in | View your stats & progress |

---

## 🎮 Common Tasks

### How to Find a Game
```
1. Go to /games
2. Type game name in search box
3. Or select genre from dropdown
4. Click "View Details" on result
```

### How to Track Game Progress
```
1. On game detail page
2. Click "Start Playing" or "Update Progress"
3. Adjust the progress slider (0-100%)
4. Enter last played date if desired
5. Click "Save Progress"
6. Visit /profile to see all tracked games
```

### How to Write a Review
```
1. On game detail page
2. Click "Write a Review"
3. Click stars to rate (1-5)
4. Type your comment (optional)
5. Click "Post Review"
6. Review appears in reviews section
```

### How to Logout
```
1. Click "Logout" in top right navigation
2. Session ends, redirected to home
3. Login again to continue
```

---

## 🐛 Troubleshooting

### Server Won't Start
**Error:** `Address already in use`
```bash
# Kill process using port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### Pages Show "Loading..." Forever
1. **Check console:**
   - Press `F12` to open Developer Tools
   - Go to **Console** tab
   - Look for red error messages
   
2. **Verify server is running:**
   - Terminal should show: `Uvicorn running on http://127.0.0.1:8000`
   
3. **Clear cache:**
   - Press `Ctrl+Shift+Delete` (or `Cmd+Shift+Delete` on Mac)
   - Clear cache and cookies
   - Refresh page

### Login Not Working
1. Verify account was created successfully
2. Check username/password are correct
3. Clear browser localStorage:
   - Open DevTools (F12)
   - Application tab → Storage → Local Storage
   - Delete `access_token` entry
   - Try login again

### Games/Reviews Not Loading
1. **Check network errors:**
   - Open DevTools → Network tab
   - Look for red failed requests
   - Note the error message

2. **Common causes:**
   - Backend not running (restart with `uvicorn app.main:app --reload`)
   - API endpoint not found (check FastAPI logs)
   - Database error (check terminal output)

### Progress Not Saving
1. Ensure you're logged in
2. Check browser console for errors
3. Verify the game exists
4. Check backend logs for database errors

---

## 💡 Tips & Tricks

### Use Browser DevTools
- **Console (F12):** See error messages
- **Network Tab:** Watch API calls
- **Application Tab:** View localStorage data
- **Inspector:** Inspect HTML/CSS

### Test Different Scenarios
```
# Register multiple accounts
- user1 / pass123
- user2 / pass123
- user3 / pass123

# Test game tracking
- Add same game with different progress
- Compare on profile page

# Test reviews
- Write multiple reviews for same game
- See them appear in reviews section
```

### API Testing (Advanced)
Use curl or Postman to test endpoints directly:
```bash
# Get all games
curl http://localhost:8000/games/

# Login
curl -X POST http://localhost:8000/login \
  -d "username=testuser&password=password123"

# View game
curl http://localhost:8000/games/1
```

---

## 📁 Project Structure Quick Reference

```
app/
├── templates/          # All HTML pages
├── static/             # CSS & JavaScript
│   ├── css/style.css  # Styling
│   └── js/            # API & Auth scripts
├── routers/            # API endpoints
├── models.py           # Database models
├── schemas.py          # Validation schemas
├── database.py         # DB connection
└── main.py            # FastAPI app & routes

tests/                  # Test files
requirements.txt        # Python dependencies
README.md              # Project README
FRONTEND.md            # Detailed docs
FRONTEND_SUMMARY.md    # Feature summary
QUICK_START.md         # This file
```

---

## 🎓 Learning Resources

### Frontend Technologies Used
- **HTML/CSS/JS:** Mozilla Developer Network (MDN)
- **Bootstrap:** https://getbootstrap.com/docs/5.3
- **Font Awesome:** https://fontawesome.com/icons
- **FastAPI:** https://fastapi.tiangolo.com
- **JWT:** https://jwt.io

### Local API Testing
```bash
# Access Swagger UI
http://localhost:8000/docs

# Access ReDoc (alternative docs)
http://localhost:8000/redoc
```

---

## ✅ Verification Checklist

Use this to verify your setup is working:

- [ ] Server starts without errors
- [ ] Home page loads at http://localhost:8000
- [ ] Can navigate all pages
- [ ] Can register new account
- [ ] Can login with credentials
- [ ] Can see games list
- [ ] Can view game details
- [ ] Can write a review
- [ ] Can track progress
- [ ] Can view profile
- [ ] Can logout
- [ ] Can login again

If all checkboxes pass, your setup is complete! ✨

---

## 🆘 Need Help?

1. **Check the documentation:**
   - `FRONTEND.md` - Comprehensive documentation
   - `README.md` - Project overview

2. **Examine error messages:**
   - Browser console (F12)
   - Terminal output
   - Network tab (F12)

3. **Check the code:**
   - Templates in `app/templates/`
   - JavaScript in `app/static/js/`
   - Styles in `app/static/css/`

---

**Happy coding! 🎮**
