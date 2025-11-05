# Website Features Guide

## Overview
This Machine Learning Notes website is a modern, interactive platform for studying ML concepts with 28 comprehensive questions across 4 units.

## Key Features

### 1. 🎨 Modern Dark Theme
- Eye-friendly dark color scheme
- Smooth animations and transitions
- Professional gradient effects
- High contrast for readability

### 2. 📱 Mobile Responsive Design
The website automatically adapts to:
- **Desktop** (1200px+): Full-width cards in grid layout
- **Tablet** (768px - 1200px): Optimized 2-column layout
- **Mobile** (< 768px): Single column, touch-friendly interface

### 3. 🔖 Bookmark System
**How it works:**
- Click the bookmark icon on any question card
- Or click the floating bookmark button on any question page
- Bookmarks are saved in browser's localStorage
- View all bookmarks by clicking the bookmark button in header
- Remove bookmarks anytime with one click

**Features:**
- Persistent across browser sessions
- Shows bookmark count in header
- Quick access to favorite questions
- Organized by most recent

### 4. 🔍 Smart Search
**Usage:**
1. Type in the search box at the top of the page
2. Results filter in real-time as you type
3. Searches through all question titles
4. Case-insensitive matching

**Tips:**
- Search for keywords like "algorithm", "bias", "ML"
- Combine with unit filters for precise results
- Clear search to see all questions again

### 5. 🏷️ Filter by Unit
**Available Filters:**
- All Questions (default)
- Unit 1: Fundamentals & KNN
- Unit 2: Applications & Classification
- Unit 3: Performance & Optimization
- Unit 4: Probability & Statistics

**How to use:**
- Click any unit tab to filter
- Combine with search for targeted results
- Active filter is highlighted in blue

### 6. 📊 Question Cards Layout
**Each card shows:**
- Question number (Q1, Q2, etc.)
- Full question text
- Unit badge
- Marks indicator (4 marks or 8 marks)
- Bookmark button

**Interaction:**
- Click anywhere on the card to view the answer
- Hover for visual feedback
- Bookmark without navigating away

### 7. 👆 Swipe Navigation (NEW!)
**How it works:**
- **Swipe left** or **drag left with mouse**: Navigate to next question
- **Swipe right** or **drag right with mouse**: Navigate to previous question
- Visual indicator shows swipe direction
- Works on both mobile and desktop

**Navigation Order:**
4Q1 → 4Q2 → 4Q3 → Q4 → Q5 → Q6 → ... → Q28

**Features:**
- Minimum swipe distance prevents accidental triggers
- Distinguishes between swipe and scroll (vertical movement ignored)
- Respects question boundaries (won't navigate past first/last)
- Smooth visual feedback with animated indicator
- Only left mouse button triggers navigation

**Usage Tips:**
- On mobile: Use natural swipe gestures
- On desktop: Click and drag horizontally
- Quick way to review multiple questions in sequence
- Works great for sequential studying

### 8. 📄 Question Pages
**Features:**
- Clean, readable content layout
- Formatted tables and code blocks
- "Back to Questions" button
- Floating bookmark button
- Swipe navigation for quick browsing
- Proper heading hierarchy
- Syntax highlighting for code

### 9. 💾 Data Persistence
**What's saved:**
- Bookmarked questions
- Bookmark timestamps
- User preferences

**Storage:**
- Uses browser's localStorage
- No server required
- Works offline after first load
- Data stays private on your device

## Technical Details

### Browser Compatibility
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Full support

### Performance
- Fast load times
- Minimal JavaScript
- Optimized CSS
- No external dependencies (except Font Awesome icons)

### Accessibility
- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Reduced motion support for accessibility

## Usage Tips

### For Students
1. **Bookmark exam-important questions** for quick revision
2. **Use search** to find topics you're studying
3. **Filter by unit** when preparing unit-wise
4. **Mobile access** for studying on the go

### For Quick Reference
1. Open the website on your phone
2. Bookmark frequently referenced questions
3. Access bookmarks panel for instant navigation
4. Search for specific concepts during exams

### For Organized Study
1. Study one unit at a time using filters
2. Bookmark completed questions
3. Track progress through bookmark count
4. Review bookmarked questions before exam

## Customization

### For Developers
The website is built with:
- **Python** (build.py): Static site generator
- **HTML/CSS**: Modern responsive design
- **JavaScript**: Interactive features
- **Markdown**: Content format

### Files to Modify
- `static/style.css`: Change colors, spacing, fonts
- `static/script.js`: Add new features or modify behavior
- `templates/base.html`: Change layout structure
- `build.py`: Modify generation logic

### Adding New Questions
1. Create a new `.md` file in root directory
2. Add entry to `QUESTION_MAP` in `build.py`
3. Run `python3 build.py`
4. New question appears on the website

## Troubleshooting

### Bookmarks not saving?
- Check if browser allows localStorage
- Try a different browser
- Clear browser cache and try again

### Search not working?
- Refresh the page
- Check browser console for errors
- Ensure JavaScript is enabled

### Mobile view issues?
- Clear browser cache
- Update to latest browser version
- Try landscape/portrait orientation

### Page not loading?
- Check internet connection (for Font Awesome icons)
- Verify all files are in correct directories
- Rebuild site with `python3 build.py`

## Future Enhancements (Possible)
- Export bookmarks feature
- Print-friendly view
- Dark/Light theme toggle
- Progress tracking
- Notes on questions
- Share functionality
- PDF export

## Support
For issues or suggestions, please open an issue on the GitHub repository.

---

**Happy Studying! 📚**
