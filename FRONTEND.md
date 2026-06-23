# GoodPlays Frontend Documentation

## Overview
A modern, responsive web frontend for the GoodPlays game review and progress tracking platform. Built with HTML5, Bootstrap 5, and Vanilla JavaScript.

## Project Structure

```
app/
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── games.html             # Games listing and search
│   ├── game-detail.html       # Game detail page
│   └── profile.html           # User profile page
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   └── js/
│       ├── api.js             # API utility functions
│       └── auth.js            # Authentication helpers
└── main.py                    # Flask/FastAPI app with route definitions
```

## Features

### 1. **Authentication**
   - User Registration: Create new account with username, email, and password
   - Login: Secure login using JWT tokens
   - Session Management: Automatic token storage in localStorage
   - Logout: Clear session and redirect to home

### 2. **Game Browsing**
   - List all games with search functionality
   - Filter by genre
   - View game details (title, developer, description, genre, release year)
   - Paginated game listing
   - Add new games (authenticated users only)

### 3. **Game Details**
   - Complete game information
   - Community reviews and ratings (1-5 stars)
   - User progress tracking
   - Write and view reviews
   - Track game completion percentage
   - Record last played date

### 4. **Progress Tracking**
   - Track completion percentage for each game
   - Record last played date/time
   - Update progress as you play
   - View all games in progress on profile

### 5. **Reviews & Ratings**
   - Write reviews with 1-5 star ratings
   - Add comments to reviews
   - View all reviews for a game
   - Star rating interactive selector

### 6. **User Profile**
   - View profile information
   - See all games in progress
   - View statistics (games in progress, reviews written)
   - Track gaming history

## Pages

### Home Page (`/`)
- Hero section with app overview
- Feature highlights
- Popular games showcase
- Call-to-action buttons for authentication

### Login Page (`/login`)
- Username and password input
- Form validation
- Error message display
- Link to registration

### Registration Page (`/register`)
- Username, email, password inputs
- Password confirmation
- Form validation
- Success redirect to login

### Games Page (`/games`)
- Search games by title or developer
- Filter by genre
- View game cards with key information
- Add new game button (authenticated)
- Responsive grid layout

### Game Detail Page (`/game/{id}`)
- Complete game information
- User progress section with progress bar
- Start/update progress tracker
- Community reviews section
- Write review button
- Game info sidebar

### Profile Page (`/profile`)
- User information display
- Statistics dashboard
- Gaming progress list with progress bars
- Reviews section

## Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with custom properties
- **Bootstrap 5**: Responsive framework
- **Font Awesome 6**: Icon library
- **Vanilla JavaScript**: No frameworks, pure JS with async/await
- **JWT**: Token-based authentication

### Backend Integration
- **RESTful API**: Calls to FastAPI endpoints
- **Local Storage**: Client-side token storage
- **Bearer Token Authentication**: JWT in Authorization header

## API Endpoints Used

```
Authentication:
POST   /login                          Login user
POST   /users/                         Register new user

Games:
GET    /games/                         List all games
GET    /games/{game_id}                Get game details
POST   /games/                         Create new game

Progress:
POST   /progress/                      Create progress entry
GET    /progress/by-user/{user_id}     Get user's progress
GET    /progress/by-user-and-game/{user_id}/{game_id}  Get specific progress
PUT    /progress/by-user-and-game/{user_id}/{game_id}  Update progress

Reviews:
POST   /reviews/                       Create review
GET    /reviews/game/{game_id}         Get game reviews
PUT    /reviews/{review_id}            Update review
DELETE /reviews/{review_id}            Delete review
```

## CSS Custom Properties

```css
--primary-color: #007bff
--secondary-color: #6c757d
--success-color: #28a745
--danger-color: #dc3545
--warning-color: #ffc107
--info-color: #17a2b8
--light-color: #f8f9fa
--dark-color: #343a40
```

## JavaScript Utilities

### api.js
```javascript
getGames(skip, limit)              // Fetch games list
getGame(id)                        // Get single game
getUser(id)                        // Get user info
getReviews(gameId, token)         // Get game reviews
getUserProgress(userId, token)    // Get user progress
```

### auth.js
```javascript
checkAuthState()                   // Update UI based on auth
logout()                           // Clear session
getAuthHeader()                    // Get auth header for requests
initializeNavigation()             // Setup nav listeners
```

## Usage

### Running the Application

1. **Start the backend server:**
```bash
cd /path/to/GoodPlays
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. **Open in browser:**
```
http://localhost:8000
```

### Navigation
- **Home**: Overview of the platform
- **Games**: Browse and search all games
- **Login/Register**: Authentication pages
- **Profile**: View your gaming activity (logged in only)

### Workflow

#### For New Users:
1. Visit home page
2. Click "Join Now" or go to `/register`
3. Create account with username, email, password
4. Redirected to login page
5. Log in with credentials
6. Start browsing games

#### For Game Discovery:
1. Navigate to Games page
2. Search by title/developer or filter by genre
3. Click "View Details" on any game
4. See full game info and reviews

#### For Progress Tracking:
1. On game detail page, click "Start Playing"
2. Set completion percentage and last played time
3. Return anytime to update progress
4. View all progress on profile page

#### For Reviews:
1. On game detail page, click "Write a Review"
2. Select star rating (1-5)
3. Add optional comment
4. Submit review
5. See your review in the reviews section

## Styling Features

### Responsive Design
- Mobile-first approach
- Bootstrap grid system
- Flexible layouts for all screen sizes
- Touch-friendly buttons and inputs

### Interactive Elements
- Hover effects on cards
- Smooth transitions
- Loading spinners
- Form validation
- Error/success alerts

### Accessibility
- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- Color contrast compliance
- Form labels and error messages

## Browser Support
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Future Enhancements
- [ ] User profile editing
- [ ] Game recommendations based on reviews
- [ ] Social features (follow users, see friends' activity)
- [ ] Achievement system
- [ ] Wishlist functionality
- [ ] Game images and covers
- [ ] Multiplayer/cooperative game tracking
- [ ] Export gaming statistics
- [ ] Dark mode toggle
- [ ] Internationalization (i18n)

## Troubleshooting

### Login Issues
- Clear browser cache and localStorage
- Check browser console for error messages
- Ensure backend server is running

### Game Data Not Loading
- Verify API endpoints are correct
- Check network tab in browser dev tools
- Ensure proper authentication token

### Progress Not Saving
- Confirm you're logged in
- Check browser console for errors
- Verify user_id matches backend

## Notes

- The frontend uses localStorage to persist authentication tokens
- Game IDs in URLs are extracted from the pathname, not query parameters
- User ID retrieval is currently set to '1' as placeholder (implement `/me` endpoint for real solution)
- All timestamps use ISO 8601 format
- Star ratings use Font Awesome icons

## Support

For issues or questions, check:
1. Browser console for error messages
2. Network tab for failed API calls
3. Backend logs for server errors
4. README.md in project root for setup instructions
