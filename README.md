# 🎓 StudyFlow

**A Student Productivity & Study Planning Web Application**

StudyFlow is a web-based productivity application designed to help students organize their academic activities in one place. It provides tools for managing notes, tracking tasks, planning study sessions, and monitoring productivity through a personalized dashboard.

The project also demonstrates containerization and CI/CD automation using Docker, Docker Hub, and GitHub Actions.

<p align="center">
  <a href="https://github.com/nahdiya-niyas/StudyFlow">GitHub Repository</a> •
  <a href="https://hub.docker.com/r/nahdiyaniyas/studyflow">Docker Hub</a> •
  <a href="https://github.com/nahdiya-niyas/StudyFlow/actions">GitHub Actions</a>
</p>

---

## ✨ Features

- 🔐 **User Authentication** – User registration and secure login.
- 📝 **Notes Management** – Create, edit, and delete personal notes.
- 📋 **Task Management** – Create and manage academic tasks.
- ✅ **Task Tracking** – Monitor pending and completed tasks.
- 📅 **Study Planner** – Organize study sessions.
- ⏱️ **Study Timer** – Use independent countdown timers for study sessions.
- 📊 **Productivity Dashboard** – View personal study activity.
- 👤 **User Profile** – Manage profile information.
- 📱 **Responsive Interface** – Access the application through a modern web interface.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Database | SQLite |
| Authentication | Flask-Login |
| ORM | Flask-SQLAlchemy |
| Password Security | Werkzeug |
| Containerization | Docker |
| Container Orchestration | Docker Compose |
| Image Registry | Docker Hub |
| CI/CD | GitHub Actions |
| Version Control | Git, GitHub |

## 🏗️ Project Architecture

StudyFlow is packaged as a Docker image and published to Docker Hub.

The GitHub Actions workflow automatically validates the Python source code, builds the Docker image, and publishes updated images to Docker Hub when changes are pushed to the `main` branch.

```text
       Developer
           |
           v
        GitHub
           |
           v
    GitHub Actions
           |
     Validate & Build
           |
           v
       Docker Hub
           |
       Pull Image
           |
           v
    Docker Compose
           |
           v
     StudyFlow App
           |
           v
      Web Browser
```

## 🐳 Run with Docker Compose (Recommended)

You can run StudyFlow without cloning the source code or manually installing Python dependencies.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine
- Docker Compose (included with current Docker Desktop installations)

### 1. Create a deployment folder

```bash
mkdir studyflow
cd studyflow
```

### 2. Download the deployment files

Download the Compose configuration and environment template:

```bash
curl -O https://raw.githubusercontent.com/nahdiya-niyas/StudyFlow/main/compose.yaml
curl -O https://raw.githubusercontent.com/nahdiya-niyas/StudyFlow/main/.env.example
```

### 3. Configure environment variables

Create your own environment file:

**Windows (Command Prompt):**

```cmd
copy .env.example .env
```

**Linux / macOS:**

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your own secret key:

```env
SECRET_KEY=your-own-random-secret-key
APP_PORT=5000
```

Keep your `.env` file private. Do not publish it or share your secret key.

### 4. Start StudyFlow

```bash
docker compose up -d
```

Docker Compose will download the published image if it is not already available locally, create the container, configure the persistent volume, and start the application.

### 5. Access the application

Open your browser:

```text
http://localhost:5000
```

That's it! 🎉

### Useful Docker Compose Commands

| Command | Description |
|---|---|
| `docker compose ps` | View running services |
| `docker compose logs -f` | View application logs |
| `docker compose stop` | Stop the application |
| `docker compose start` | Start the application again |
| `docker compose down` | Stop and remove the container |
| `docker compose pull` | Download the latest image |
| `docker compose up -d` | Start the application |

**Data persistence:** StudyFlow uses a named Docker volume to store its SQLite database. Your application data is retained when the container is recreated or the Compose application is stopped and started again. Avoid `docker compose down -v` if you want to preserve your data.

---

## 📦 Docker Image

The published Docker image is available on Docker Hub.

**Repository:** [nahdiyaniyas/studyflow](https://hub.docker.com/r/nahdiyaniyas/studyflow)

Pull the latest image:

```bash
docker pull nahdiyaniyas/studyflow:latest
```

The image is built for `linux/amd64`.

### Available Tags

| Tag | Description |
|---|---|
| `latest` | Most recently published image |
| Commit SHA | Image associated with a specific Git commit |

---

## ⚙️ CI/CD Pipeline

StudyFlow uses GitHub Actions to automate the image build and publishing process.

### Workflow Triggers

- **Push to `main`:** Validates the project, builds the Docker image, and publishes it to Docker Hub.
- **Pull request to `main`:** Validates the project and builds the Docker image without publishing it.
- **Manual execution:** Allows the workflow to be triggered manually.

### Pipeline Steps

1. Check out the repository.
2. Set up Python.
3. Install project dependencies.
4. Check Python source-code syntax.
5. Set up Docker Buildx.
6. Authenticate with Docker Hub when publishing.
7. Build the Docker image.
8. Push the image to Docker Hub on pushes to `main`.

The published image is tagged with `latest` and the corresponding Git commit SHA.

**View workflow runs:** [StudyFlow GitHub Actions](https://github.com/nahdiya-niyas/StudyFlow/actions)

---

## 💻 Run Locally (Development)

If you want to explore or modify the source code, follow these steps.

### Prerequisites

- Python 3.14
- Git

### 1. Clone the repository

```bash
git clone https://github.com/nahdiya-niyas/StudyFlow.git
cd StudyFlow
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```cmd
venv\Scripts\activate
```

On Linux / macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-own-random-secret-key
```

### 5. Run the application

```bash
python main.py
```

Open the local address shown in your terminal (normally `http://localhost:5000`).

---

## 📁 Project Structure

```text
StudyFlow/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── website/
│   ├── static/
│   │   ├── css/
│   │   └── index.js
│   │
│   ├── templates/
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   ├── planner.py
│   ├── tasks.py
│   └── views.py
│
├── kubernetes/
│   └── Kubernetes configuration files
│
├── .dockerignore
├── .env.example
├── .gitignore
├── compose.yaml
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```

## 📚 Important Resources & Documentation

| Resource | Link |
|---|---|
| Source Code | [GitHub Repository](https://github.com/nahdiya-niyas/StudyFlow) |
| Docker Image | [Docker Hub](https://hub.docker.com/r/nahdiyaniyas/studyflow) |
| Docker Compose Configuration | [compose.yaml](https://github.com/nahdiya-niyas/StudyFlow/blob/main/compose.yaml) |
| Environment Template | [.env.example](https://github.com/nahdiya-niyas/StudyFlow/blob/main/.env.example) |
| Dockerfile | [Dockerfile](https://github.com/nahdiya-niyas/StudyFlow/blob/main/Dockerfile) |
| CI/CD Workflow | [ci-cd.yml](https://github.com/nahdiya-niyas/StudyFlow/blob/main/.github/workflows/ci-cd.yml) |
| Workflow Execution History | [GitHub Actions](https://github.com/nahdiya-niyas/StudyFlow/actions) |

## 🔒 Security Notes

- Application secrets are provided through environment variables.
- The `.env` file is excluded from version control and the Docker build context.
- Users should generate their own secret key.
- Docker Hub credentials are stored as GitHub repository secrets for automated publishing.
- Never commit private credentials, access tokens, or production secrets.

## 👩‍💻 Author

**Nahdiya Niyas**

Bachelor of Information and Communication Technology (Hons) Student

[GitHub Profile](https://github.com/nahdiya-niyas)

---

<p align="center">
  ⭐ If you find StudyFlow interesting, feel free to explore the repository!
</p>