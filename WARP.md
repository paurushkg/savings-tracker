# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Development Commands

### Initial Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate
```

### Daily Development
```bash
# Start development server
python manage.py runserver

# Run migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Create Django superuser (for admin access)
python manage.py createsuperuser

# Collect static files (if needed for production)
python manage.py collectstatic
```

### Testing
```bash
# Run Django tests
python manage.py test

# Run specific app tests
python manage.py test tracker

# Run with verbose output
python manage.py test --verbosity=2
```

## Architecture Overview

This is a single-page Django application for tracking savings progress toward ₹1,00,000 using an interactive grid interface.

### Core Components

**SavingsBox Model** (`tracker/models.py`):
- Represents individual savings boxes with random values (₹200, ₹500, or ₹1000)
- Uses `initialize_boxes()` classmethod to generate boxes totaling exactly ₹1,00,000
- Tracks position in grid and saved status per box

**AJAX-Driven Frontend**:
- Single-page application with no page reloads
- JavaScript handles box toggling via `/toggle/<box_id>/` endpoint
- Real-time progress updates and celebrations
- Wooden theme with responsive CSS Grid layout

**Key Views** (`tracker/views.py`):
- `index()`: Main view rendering the savings grid
- `toggle_box()`: AJAX endpoint for marking boxes as saved/unsaved
- `reset_progress()`: Clears all saved progress
- `initialize_boxes_view()`: Generates new challenge with fresh box values

### URL Structure
- `/`: Main savings tracker interface
- `/toggle/<box_id>/`: AJAX endpoint for box state changes
- `/reset/`: Reset all progress
- `/initialize/`: Generate new challenge
- `/admin/`: Django admin interface

### Data Flow
1. Page loads → Check if boxes exist, initialize if empty
2. User clicks box → AJAX call to toggle endpoint
3. Server updates box state → Returns updated progress data
4. Frontend updates progress bar and celebrates milestones
5. All boxes saved → Confetti celebration for goal achievement

### Customization Points
- **Target Amount**: Modify `target_amount` variable in `SavingsBox.initialize_boxes()`
- **Box Values**: Change `BOX_VALUES` list in `SavingsBox` model
- **Styling**: Update CSS in `tracker/static/tracker/css/style.css`
- **Animations**: Modify JavaScript in `tracker/static/tracker/js/main.js`

### Database
- Uses SQLite with single `SavingsBox` table
- Auto-generates approximately 100-150 boxes to reach ₹1,00,000 total
- Each box tracks value, position, saved status, and creation timestamp