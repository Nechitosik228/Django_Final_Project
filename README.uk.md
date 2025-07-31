# Zentour

![Logo](zentour/images/logo.jpg)

## Опис
**Zentour** – це веб-додаток для бронювання турів, створений як зручний інструмент для туристів і туроператорів.  
Основна мета проєкту – спростити процес пошуку, бронювання та управління туристичними подорожами.

## Основні можливості
- Переглядати доступні тури з детальним описом і візуалізацією;
- Керувати власним профілем і балансом;
- Бронювати тури та відслідковувати транзакції;
- Туроператорам створювати власні тури після підтвердження статусу **Super User**.

Проєкт побудований на **Django**  він є легко розширюваним та зручним для подальшої інтеграції з іншими сервісами.

## Технології

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
## Інсталяція
Щоб розпочати роботу з **Zentour**, виконайте такі кроки:

1. **Скопіювати репозиторій:**

    ```bash
    git clone https://github.com/Nechitosik228/Django_Final_Project.git
    ```
2. **Створити віртуальне середовище (venv):**

+ Для Windows (PowerShell):
    ```powershell
    python -m venv .venv
    ```
+ Для GNU/Linux & macOS:
    ```bash
    python3 -m venv .venv
    ```
3. **Активувати віртуальне середовище:**
+ Для Windows (PowerShell):
    ```powershell
    .\.venv\Scripts\activate.ps1    
    ```
+ Для GNU/Linux and macOS:
    ```bash
    source .venv\bin\activate
    ```
4. **Встановіть необхідні залежності:**
    ```bash
    cd zentour
    pip install -r requirements.txt 
    ```
5. **Виконати міграцію бази даних:**
    ```bash
    python manage.py migrate
    ```
6. **Запустіть сервер:**
    ```bash
    python manage.py runserver
    ```
## Додатково

![Schema](zentour/images/zentour.drawio.png)

---
# Переклад [Англійською](README.md)
