# Zentour

![Logo](zentour/images/logo.jpg)

## About
**Zentour** is a web application for booking tours, created as a convenient tool for tourists and tour operators.
The main goal of the project is to simplify the process of searching, booking, and managing tourist trips.

## Main features
- View available tours with detailed descriptions and visualisations;
- Manage your profile and balance;
- Book tours and track transactions;
- Tour operators can create their own tours after confirming their **Super User** status.

The project is built on **Django**, making it easily expandable and convenient for further integration with other services.

## Technologies

### Backend

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

### Frontend

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

### DevOps

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)


## Installation
To get started with **Zentour**, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Nechitosik228/Django_Final_Project.git
    ```
2. **Create a virtual environment (venv):**

+ For Windows (PowerShell):
    ```powershell
    python -m venv .venv
    ```
+ For GNU/Linux & macOS:
    ```bash
    python3 -m venv .venv
    ```
3. **Activate the virtual environment:**
+ For Windows (PowerShell):
    ```powershell
    .\.venv\Scripts\activate.ps1    
    ```
+ For GNU/Linux and macOS:
    ```bash
    source .venv\bin\activate
    ```
4. **Install the required dependencies:**
    ```bash
    cd zentour
    pip install -r requirements.txt 
    ```
5. **Run database migrations:**
    ```bash
    python manage.py migrate
    ```
6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Run Docker
1. **Create image:**
    ```bash
    docker build -t your_app_name .
    ```
2. **Run**
    ```bash
    docker run -p 8080:8080 zentour
    ```

## Project structure
```
Django_Final_Project
├─ LICENSE
├─ README.md
├─ README.uk.md
├─ tree.txt
└─ zentour
   ├─ .dockerignore
   ├─ accounts
   │  ├─ admin.py
   │  ├─ apps.py
   │  ├─ forms.py
   │  ├─ migrations
   │  │  ├─ 0001_initial.py
   │  │  ├─ 0002_alter_profile_avatar_alter_profile_user.py
   │  │  ├─ 0003_alter_profile_avatar.py
   │  │  ├─ 0004_alter_profile_avatar.py
   │  │  ├─ 0005_transaction.py
   │  │  ├─ 0006_transaction_category_transaction_status.py
   │  │  ├─ 0007_alter_transaction_options.py
   │  │  └─ __init__.py
   │  ├─ models.py
   │  ├─ signals.py
   │  ├─ templates
   │  │  └─ accounts
   │  │     ├─ balance.html
   │  │     ├─ edit_profile.html
   │  │     ├─ emails
   │  │     │  └─ reset.html
   │  │     ├─ login.html
   │  │     ├─ password_change.html
   │  │     ├─ password_change_done.html
   │  │     ├─ profile.html
   │  │     ├─ register.html
   │  │     ├─ reset_password
   │  │     │  ├─ complete.html
   │  │     │  ├─ confirm.html
   │  │     │  ├─ done.html
   │  │     │  └─ form.html
   │  │     ├─ superuser.html
   │  │     └─ transactions.html
   │  ├─ test
   │  │  ├─ fixtures.py
   │  │  ├─ test_endpoints.py
   │  │  ├─ test_forms.py
   │  │  ├─ test_models.py
   │  │  └─ __init__.py
   │  ├─ urls.py
   │  ├─ views.py
   │  └─ __init__.py
   ├─ conftest.py
   ├─ Dockerfile
   ├─ images
   │  ├─ logo.jpg
   │  └─ zentour.drawio.png
   ├─ manage.py
   ├─ pytest.ini
   ├─ requirements.txt
   ├─ tours
   │  ├─ admin.py
   │  ├─ apps.py
   │  ├─ forms.py
   │  ├─ migrations
   │  │  ├─ 0001_initial.py
   │  │  ├─ 0002_cartitem_order_orderitem.py
   │  │  ├─ 0003_rename_image_path_tour_image.py
   │  │  ├─ 0004_tour_user.py
   │  │  ├─ 0005_alter_tour_image.py
   │  │  ├─ 0006_review.py
   │  │  ├─ 0007_remove_tour_available.py
   │  │  ├─ 0008_alter_cart_user_alter_orderitem_items.py
   │  │  ├─ 0008_alter_cart_user_alter_review_tour.py
   │  │  ├─ 0009_remove_orderitem_items_orderitem_order.py
   │  │  ├─ 0010_merge_20250718_0720.py
   │  │  ├─ 0011_tour_buyers.py
   │  │  ├─ 0012_remove_tour_buyers_alter_tour_discount_and_more.py
   │  │  ├─ 0013_boughttour_price.py
   │  │  ├─ 0014_remove_orderitem_price.py
   │  │  └─ __init__.py
   │  ├─ models.py
   │  ├─ static
   │  │  └─ js
   │  │     └─ review_star.js
   │  ├─ templates
   │  │  └─ tours
   │  │     ├─ base.html
   │  │     ├─ cart.html
   │  │     ├─ checkout.html
   │  │     ├─ create_tour.html
   │  │     ├─ delete_review.html
   │  │     ├─ delete_tour.html
   │  │     ├─ edit_tour.html
   │  │     ├─ home.html
   │  │     ├─ tour_detail.html
   │  │     └─ users_tours.html
   │  ├─ test
   │  │  ├─ fixtures.py
   │  │  ├─ test_endpoints.py
   │  │  ├─ test_forms.py
   │  │  ├─ test_models.py
   │  │  └─ __init__.py
   │  ├─ urls.py
   │  ├─ utils
   │  │  ├─ calculate_star.py
   │  │  ├─ transaction.py
   │  │  └─ __init__.py
   │  ├─ views.py
   │  └─ __init__.py
   └─ zentour
      ├─ asgi.py
      ├─ settings.py
      ├─ urls.py
      ├─ wsgi.py
      └─ __init__.py
```
## Reports

![Schema](zentour/images/zentour.drawio.png)

---
# Translation to [Ukrainian](README.uk.md)

