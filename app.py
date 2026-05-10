from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "startup_secret"

users = []

jobs = [
    {
        "title": "Python Intern",
        "company": "Google",
        "location": "Bishkek",
        "description": "Стажировка для начинающих Python разработчиков. Изучение Django, Flask и работы с базами данных.",
        "posted_by": "system"
    },
    {
        "title": "Senior Python Developer",
        "company": "Yandex",
        "location": "Moscow",
        "description": "Ищем опытного Python разработчика для работы над высоконагруженными проектами. Требования: опыт от 3 лет, знание asyncio, PostgreSQL.",
        "posted_by": "system"
    },
    {
        "title": "Frontend Developer (React)",
        "company": "Meta",
        "location": "Remote",
        "description": "Разработка пользовательских интерфейсов на React.js. Опыт работы с TypeScript и Next.js приветствуется.",
        "posted_by": "system"
    },
    {
        "title": "Data Scientist",
        "company": "OpenAI",
        "location": "San Francisco",
        "description": "Поиск и анализ данных, построение ML моделей. Требования: Python, Pandas, Scikit-learn, TensorFlow.",
        "posted_by": "system"
    },
    {
        "title": "DevOps Engineer",
        "company": "Amazon",
        "location": "Remote",
        "description": "Настройка CI/CD pipelines, работа с AWS, Docker, Kubernetes. Опыт от 2 лет обязателен.",
        "posted_by": "system"
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    filtered_jobs = jobs

    if request.method == "POST":
        search = request.form.get("user_input", "").lower()

        filtered_jobs = [
            job for job in jobs
            if search in job["title"].lower()
            or search in job["company"].lower()
            or search in job["location"].lower()
        ]

    user = session.get("user")
    role = session.get("role")
    return render_template("index.html", jobs=filtered_jobs, user=user, role=role)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        for user in users:
            if user["username"] == username:
                return "Пользователь с таким именем уже существует!"

        users.append({
            "username": username,
            "password": password,
            "role": role
        })

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                session["role"] = user["role"]
                return redirect(url_for("index"))

        return "Неверный логин или пароль!"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/add_job", methods=["GET", "POST"])
def add_job():
    if "user" not in session or session.get("role") != "employer":
        return "Доступ только для работодателей. <a href='/'>Вернуться на главную</a>"

    if request.method == "POST":
        title = request.form.get("title")
        company = request.form.get("company")
        location = request.form.get("location")
        description = request.form.get("description")

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "posted_by": session.get("user")
        })

        return redirect(url_for("index"))

    return render_template("add_job.html")


if __name__ == "__main__":
    app.run(debug=True)
