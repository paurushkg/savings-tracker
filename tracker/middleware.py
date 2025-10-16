from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.middleware.csrf import get_token


class PasscodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.PASSCODE = "bachat"

    def __call__(self, request):
        # Skip passcode check for admin and static files
        if (request.path.startswith('/admin/') or 
            request.path.startswith('/static/') or
            request.path == '/passcode/'):
            return self.get_response(request)

        # Check if user is already authenticated with session
        if request.session.get('authenticated'):
            return self.get_response(request)

        # If POST request with passcode
        if request.method == 'POST' and 'passcode' in request.POST:
            entered_passcode = request.POST.get('passcode')
            if entered_passcode == self.PASSCODE:
                request.session['authenticated'] = True
                return self.get_response(request)
            else:
                return self.render_passcode_form(request, error="Incorrect passcode")

        # Show passcode form for all other requests
        return self.render_passcode_form(request)

    def render_passcode_form(self, request, error=None):
        csrf_token = get_token(request)
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Enter Passcode - Savings Tracker</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Poppins', sans-serif; 
                    background: linear-gradient(135deg, #8B4513 0%, #A0522D 25%, #CD853F 50%, #D2B48C 75%, #F5DEB3 100%); 
                    min-height: 100vh; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    padding: 20px;
                }}
                .passcode-container {{ 
                    background: rgba(255, 255, 255, 0.95); 
                    border-radius: 20px; 
                    padding: 40px; 
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); 
                    backdrop-filter: blur(10px); 
                    border: 2px solid rgba(139, 69, 19, 0.2);
                    max-width: 400px;
                    width: 100%;
                    text-align: center;
                }}
                .title {{ 
                    font-size: 2rem; 
                    font-weight: 700; 
                    color: #8B4513; 
                    margin-bottom: 10px; 
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1); 
                }}
                .subtitle {{ 
                    font-size: 1rem; 
                    color: #A0522D; 
                    margin-bottom: 30px; 
                }}
                .form-group {{ 
                    margin-bottom: 20px; 
                    text-align: left; 
                }}
                label {{ 
                    display: block; 
                    margin-bottom: 8px; 
                    font-weight: 600; 
                    color: #8B4513; 
                }}
                input[type="password"] {{ 
                    width: 100%; 
                    padding: 15px; 
                    border: 2px solid #CD853F; 
                    border-radius: 8px; 
                    font-size: 1rem; 
                    font-family: inherit; 
                    background: rgba(255, 255, 255, 0.9);
                    transition: border-color 0.3s ease;
                }}
                input[type="password"]:focus {{ 
                    outline: none; 
                    border-color: #8B4513; 
                    box-shadow: 0 0 0 3px rgba(139, 69, 19, 0.1); 
                }}
                .submit-btn {{ 
                    width: 100%; 
                    padding: 15px; 
                    background: #4ECDC4; 
                    color: white; 
                    border: none; 
                    border-radius: 8px; 
                    font-size: 1rem; 
                    font-weight: 600; 
                    cursor: pointer; 
                    transition: all 0.3s ease; 
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
                }}
                .submit-btn:hover {{ 
                    background: #45B7AF; 
                    transform: translateY(-2px); 
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); 
                }}
                .error {{ 
                    background: #FF6B6B; 
                    color: white; 
                    padding: 10px; 
                    border-radius: 5px; 
                    margin-bottom: 20px; 
                    font-weight: 500; 
                }}
                .hint {{ 
                    margin-top: 20px; 
                    font-size: 0.85rem; 
                    color: #A0522D; 
                    font-style: italic; 
                }}
            </style>
        </head>
        <body>
            <div class="passcode-container">
                <h1 class="title">₹1,00,000 Savings Tracker</h1>
                <p class="subtitle">Please enter the passcode to continue</p>
                
                {"<div class='error'>" + error + "</div>" if error else ""}
                
                <form method="POST">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                    <div class="form-group">
                        <label for="passcode">Passcode:</label>
                        <input type="password" id="passcode" name="passcode" required autofocus>
                    </div>
                    <button type="submit" class="submit-btn">Enter Savings Tracker</button>
                </form>
                
                <div class="hint">🔒 Protected access to your savings challenge</div>
            </div>
        </body>
        </html>
        """.format(csrf_token=csrf_token)
        return HttpResponse(html)
