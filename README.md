# ₹1,00,000 Savings Tracker

A beautiful and responsive single-page Django application for tracking savings with a wooden-themed design inspired by traditional savings charts.

## Features

- **Interactive Savings Grid**: Click boxes to mark amounts as saved
- **Random Box Values**: Boxes contain ₹200, ₹500, or ₹1000 amounts
- **Progress Tracking**: Visual progress bar and percentage counter
- **Responsive Design**: Mobile-friendly layout with wooden theme
- **Smooth Animations**: Celebratory effects when saving money
- **Goal Achievement**: Special confetti celebration when reaching ₹1,00,000

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Django 5.0+

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd savings-tracker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Open your browser and visit:**
   ```
   http://127.0.0.1:8000
   ```

## How to Use

1. **Start Saving**: Click on any box to mark that amount as saved
2. **Track Progress**: Watch the progress bar fill up as you save more
3. **Reset Progress**: Use the "Reset Progress" button to clear all saved amounts
4. **New Challenge**: Use "New Challenge" to generate a fresh set of boxes
5. **Reach Your Goal**: Complete all boxes to trigger the celebration!

## Technical Details

### Project Structure
```
savings-tracker/
├── tracker/                 # Main Django app
│   ├── models.py           # SavingsBox model
│   ├── views.py            # Views for handling requests
│   ├── urls.py             # URL patterns
│   ├── templates/tracker/   # HTML templates
│   └── static/tracker/     # CSS and JavaScript
├── savings_tracker/        # Django project settings
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

### Key Components

- **SavingsBox Model**: Stores individual box values and saved status
- **AJAX Integration**: Smooth updates without page reloads  
- **Responsive CSS Grid**: Adapts to different screen sizes
- **Wooden Theme**: Beautiful gradients and textures

## Customization

### Changing Target Amount
Edit the `target_amount` in `tracker/models.py` (line 22):
```python
target_amount = 100000  # Change to your desired amount
```

### Box Values
Modify `BOX_VALUES` in `tracker/models.py` (line 7):
```python
BOX_VALUES = [200, 500, 1000]  # Add or change values
```

### Styling
Update colors and themes in `tracker/static/tracker/css/style.css`

## Development

To make changes to the application:

1. Modify the code as needed
2. Run migrations if you changed models:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Restart the development server

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Requires JavaScript enabled

## License

This project is open source and available under the MIT License.

---

**Happy Saving! 💰**