# 🚀 Hello World Static Web App on Minikube with NGINX Reverse Proxy

This project demonstrates deploying a simple static web application using **Flask** and **HTML** on **Minikube** running on an **AWS EC2 instance**. The app is exposed publicly using **NGINX reverse proxy**, and includes a complete **CI/CD pipeline with GitHub Actions**.

---

## ✅ Project Highlights

- 🐳 Containerized Flask app with static HTML page (Header + Footer)
- 🔁 CI/CD using GitHub Actions
- ☸️ Kubernetes Deployment via Minikube (running inside EC2)
- 🌐 NGINX reverse proxy to expose app via EC2 public IP
- 📦 Docker image build and save as artifact

---

## 🗂 Project Structure

```bash
hello-k8s-app/
├── app.py                 # Flask app serving HTML
├── index.html            # HTML page with header & footer
├── requirements.txt      # Python dependencies
├── Dockerfile            # Builds the container image
├── k8s/
│   ├── deployment.yaml   # K8s Deployment
│   └── service.yaml      # K8s NodePort Service
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # GitHub Actions workflow
├── README.md             # You're reading this!
```

---

## 🌐 App Description

The app displays a simple HTML page with:
- A styled header (`blue` background, white bold text)
- A centered body message: **"Hello, World from Kubernetes!"**
- A footer with copyright

---

## 🧑‍💻 How to Run Locally (Optional)

```bash
docker build -t hello-world-app .
docker run -p 5000:5000 hello-world-app
```
Visit: [http://localhost:5000](http://localhost:5000)

---

## 🔧 GitHub Actions CI/CD Pipeline

File: `.github/workflows/ci-cd.yml`

### What It Does:
- ✅ Lints Python code with flake8
- 🐳 Builds Docker image
- 📦 Saves image as tar file locally (`docker-output/`)
- ☁️ Uploads as GitHub Action artifact

No Docker Hub push is required for this setup.

---

## ☸️ Deploying to Minikube on EC2

### 📌 Step 1: SSH into your EC2
```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### 📌 Step 2: Set up Minikube environment
```bash
eval $(minikube docker-env)
```

### 📌 Step 3: Build Docker image for Minikube
```bash
docker build -t hello-world-app .
```

### 📌 Step 4: Apply Kubernetes manifests
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 📌 Step 5: Get Minikube IP
```bash
minikube ip
```
Access app via:
```bash
http://<minikube-ip>:30007
```

---

## 🌐 Exposing via NGINX Reverse Proxy

### 📌 Install NGINX
```bash
sudo apt install nginx -y
```

### 📌 Update NGINX default config
```nginx
server {
    listen 80;
    location / {
        proxy_pass http://192.168.49.2:30007;  # Replace with your Minikube IP
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 📌 Restart NGINX
```bash
sudo systemctl restart nginx
```

✅ Now your app is accessible via:
```bash
http://<EC2_PUBLIC_IP>
```

> Ensure EC2 Security Group has port **80** open to `0.0.0.0/0`

---

## 📸 Screenshot
![screenshot](./screenshot.png)

---

## 🧪 Troubleshooting

- 🔁 Pod stuck in `Pending`? Run `kubectl get nodes` — Minikube might need a restart
- ❌ NGINX shows 502? Check if the app is accessible on `minikube ip:30007`
- 🔐 Still can't access? Open EC2 ports 80 and 30007

---

## 🙌 Author
**Manukumarkc** — DevOps Cloud Engineer Aspirant

---

## ✅ To-Do / Next Steps
- Push Docker image to Docker Hub
- Add Trivy scanning for image security
- Automate EC2 setup using Bash or Terraform

---

This project showcases your DevOps fundamentals — well done! 🚀

