from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from functools import wraps

# Move the error HTML to a Django template (recommended for maintainability)
ERROR_HTML = ''' 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>403 Forbidden</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <style>
    body {
      margin: 0;
      padding: 0;
      background: #1d1d1d;
      font-family: 'Arial', sans-serif;
      color: #fff;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
    }

    .container {
      text-align: center;
    }

    .error-code {
      font-size: 8rem;
      font-weight: bold;
      color: #e74c3c;
      margin: 0;
    }

    .error-message {
      font-size: 2rem;
      margin: 20px 0;
      color: #ecf0f1;
    }

    .icon {
      font-size: 6rem;
      margin-bottom: 20px;
      color: #e74c3c;
      transform-origin: center;
    }

    .btn {
      display: inline-block;
      margin-top: 20px;
      padding: 10px 20px;
      font-size: 1.2rem;
      color: #fff;
      background: #e74c3c;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      text-decoration: none;
      transition: background 0.3s ease;
    }

    .btn:hover {
      background: #c0392b;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="icon">🚫</div>
    <h1 class="error-code">403</h1>
    <p class="error-message">You don't have permission to access this page.</p>
    <a href="{% url 'home' %}" class="btn">Go Home</a>
  </div>

  <script>
    // GSAP Animations
    gsap.from(".icon", { 
      duration: 1, 
      scale: 0.5, 
      rotation: 360, 
      ease: "elastic.out(1, 0.3)" 
    });

    gsap.from(".error-code", { 
      duration: 1.2, 
      opacity: 0, 
      y: -50, 
      ease: "power4.out", 
      delay: 0.5 
    });

    gsap.from(".error-message", { 
      duration: 1, 
      opacity: 0, 
      y: 30, 
      ease: "power2.out", 
      delay: 1 
    });

    gsap.from(".btn", { 
      duration: 1, 
      opacity: 0, 
      scale: 0.8, 
      ease: "back.out(1.7)", 
      delay: 1.5 
    });

    gsap.to("body", { 
      backgroundColor: "#2c3e50", 
      duration: 2, 
      delay: 0.5 
    });
  </script>
</body>
</html>

'''

def is_user(user_role):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user  # get the current user object

            if user_role == 'student' and not getattr(user, 'is_student', False):
                return HttpResponseForbidden(ERROR_HTML)
            elif user_role == 'teacher' and not getattr(user, 'is_teacher', False):
                return HttpResponseForbidden(ERROR_HTML)
            elif user_role == 'admin' and not user.is_superuser:
                return HttpResponseForbidden(ERROR_HTML)
            
            # If all checks pass, execute the original view
            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
