# 🎓 StudyFlow

**A Student Productivity Web Application | Docker | CI/CD | Kubernetes**

StudyFlow is a web-based productivity application that helps students manage notes, tasks, and study sessions in one place.

This project also demonstrates practical DevOps concepts through Docker containerization, GitHub Actions CI/CD automation, Docker Hub publishing, and Kubernetes deployment configurations.

## ✨ Features

- 🔐 User registration and authentication
- 📝 Create, edit, and delete notes
- 📋 Task management and progress tracking
- 📅 Study session planning
- ⏱️ Study session countdown timers
- 👤 User profile management
- 📊 Productivity dashboard
- 📱 Responsive interface

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| Authentication | Flask-Login |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Image Registry | Docker Hub |
| Orchestration | Kubernetes, Minikube |

## 🐳 Run with Docker

StudyFlow is available as a public Docker image.

**Docker Hub:** [nahdiyaniyas/studyflow](https://hub.docker.com/r/nahdiyaniyas/studyflow)

Pull the image:

```bash
docker pull nahdiyaniyas/studyflow:latest
```

Create a `.env` file with your own secret key:

```env
SECRET_KEY=your-own-random-secret
```

Run the container:

```bash
docker run -d \
  --name studyflow \
  -p 5000:5000 \
  --env-file .env \
  -v studyflow-data:/app/instance \
  nahdiyaniyas/studyflow:latest
```

Access the application at `http://localhost:5000`.

**Requirements:** Docker installed on your machine. No source-code download is required to run the published image.

## ⚙️ CI/CD Pipeline

GitHub Actions automates the build and publishing process whenever code is pushed to the `main` branch.

**Pipeline workflow:**

```text
GitHub Push
    |
    v
Install Python Dependencies
    |
    v
Python Syntax Validation
    |
    v
Build Docker Image
    |
    v
Authenticate with Docker Hub
    |
    v
Publish Docker Image
```

- Automated dependency installation and Python syntax validation.
- Docker image build using GitHub Actions.
- Secure authentication through GitHub repository secrets.
- Automatic publishing to Docker Hub.
- Versioned images using `latest` and commit SHA tags.

**Workflow:** [GitHub Actions](https://github.com/nahdiya-niyas/StudyFlow/actions)

## ☸️ Kubernetes

Kubernetes configuration files are included to demonstrate container orchestration.

The configurations cover:

- Namespace
- Application deployment
- ConfigMap
- Persistent volume
- Secret configuration

Deployment requires a separately configured Kubernetes cluster and the required Kubernetes Secret.

```bash
kubectl apply -f kubernetes/
```

Check deployment status:

```bash
kubectl get pods
```

## 🔐 Security

- Private `.env` files are excluded from Git and Docker images.
- Runtime environment variables are supplied when starting containers.
- Docker Hub credentials are stored securely using GitHub repository secrets.
- Kubernetes Secrets are configured separately.

## 🎯 Project Goals

Built to gain practical experience in full-stack application development and DevOps practices, including containerization, CI/CD automation, image publishing, and container orchestration.

## 👩‍💻 Author

**Nahdiya Niyas**  
Bachelor of Information and Communication Technology Undergraduate  
University of Sri Jayewardenepura

---

⭐ Feel free to explore the repository and Docker Hub image.
