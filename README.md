# Orwell Cyberspace

## Requirements

```
Django==2.1.2
Pillow==5.3.0
djangorestframework==3.9.0
django-paypal==0.5.0
social-auth-app-django==3.1.0
pycryptodome==3.7.2
sorl-thumbnail==12.5.0
gunicorn==19.9.*
```
## Components

- Django
- Django REST framework
- Semantic-UI
- jQuery
- Docker

## Features

**For buyer:**

- Sign in / up / out 
- Using Google Account to Login
- Change password
- Place order(Guest or After Login)
- Pay
  - Alipay / Paypal
- Review purchase history

**For Staff:**

- Product Management
  - Add / Delete / Modify product & category

**For Admin:**

- User Management
  - Add / Delete / Modify normal user & staff

## Site Design

- Search Engine Optimized URLs

- Google oAuth 2.0

- Automatic image resizing for product images

- Dynamically update the shopping list via AJAX

- For Security:
  - XSS Mitigation
  - CSRF Mitigation
  - SQLi Mitigation
  - HTTPS

- Easily deployment by dockerizing the whole site


