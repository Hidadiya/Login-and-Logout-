# Django-Based Login & Registration Portal

A simple **Django-based authentication system** with **email verification via OTP (One-Time Password)**.  
Users must verify their email during signup by entering an OTP sent to their email before they can log in.  
The project also includes **login, logout, reCAPTCHA protection, OTP resend with cooldowns, and account lockouts**.  

---

## 🚀 Features  

- ✅ User Signup with Email Verification  
- ✅ OTP sent to user’s email (expires in 1 minute)  
- ✅ OTP Resend option with 1-minute cooldown  
- ✅ Maximum of 3 OTP resends (locks user for 2 hours if exceeded)  
- ✅ Login with username & password (protected with reCAPTCHA)  
- ✅ Logout & simple home page  
- ✅ Session handling for secure OTP flow  

---

## 🛠️ Technologies Used  

- [Django](https://www.djangoproject.com/) (Backend Framework)  
- [SQLite](https://www.sqlite.org/) (Default Database, can be replaced with PostgreSQL/MySQL)  
- [Google reCAPTCHA](https://www.google.com/recaptcha/) (Bot protection on login)  
- [Django Messages Framework](https://docs.djangoproject.com/en/stable/ref/contrib/messages/) (For feedback messages)  
- HTML Templates + Basic CSS  

---

## 📂 Project Structure  

    User_Registration/
    │── User/
    │   ├── migrations/
    │   ├── templates/
    │   │   ├── base.html
    │   │   ├── login.html
    │   │   ├── signup.html
    │   │   ├── verify_otp.html
    │   │   └── home.html
    |   |── static/css
    |   |   ├── simple.css
    │   ├── forms.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │── auth_system/   # Django project settings
    │ 
    │── manage.py
    │── README.md
    │── requirements.txt



---

## ⚙️ Installation & Setup  

### 1. Clone the Repository  

```bash
git clone https://github.com/your-username/django-otp-auth.git
cd django-otp-auth


### 2. Create Virtual Environment

    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate     # On Windows


### 3. Install Dependencies

    pip install -r requirements.txt

### 4. Configure Settings
    Open settings.py and configure your email backend for OTP sending:

        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True
        EMAIL_HOST_USER = 'your_email@gmail.com'
        EMAIL_HOST_PASSWORD = 'your_email_password_or_app_password'


    Add your Google reCAPTCHA keys in settings.py:

        RECAPTCHA_PUBLIC_KEY = 'your-site-key'
        RECAPTCHA_PRIVATE_KEY = 'your-secret-key'


### 5. Apply Migrations

    python manage.py migrate


### 6. Run Server

    python manage.py runserver


## 📸 Screenshots  

### 🔹 Signup Page  
![Signup](static/images/signuppage.png)  

### 🔹 OTP Verification  
![OTP](static/images/otppage.png)  

### 🔹 Login Page with reCAPTCHA  
![Login](static/images/loginpage.png)  

### 🔹 Home Page  
![Home](static/images/homepage.png)  


## License

This project is intended for educational purposes only.

Usage Terms

You may use, modify, and share this code for learning, teaching, or academic projects.
Commercial use, redistribution, or deployment in production environments is not permitted without explicit permission.
This project is provided "as is" with no warranties or guarantees.
If you wish to use this project beyond an educational scope, please contact the author for permission.


👨‍💻 Author

Developed by Hidayathulla 🚀
Feel free to fork, contribute, and star ⭐ this repo if you find it useful.







