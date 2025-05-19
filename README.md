**#Hello All, This is a Explanation of Project for Hosting Static Web App on MiniKube inside AWS EC2 with NGINX Reverse Proxy.**
 
**Access application on URL:** http://25.25.25.99

This Project Demonstrates Deploying  Static Web page application on HTML using Flask Python Frame work inside **Minikube Cluster** running on **AWS EC2 Instance with T2.large** Configuration, This Static Web page is exposed to public using NGINX reverse proxy and includes a Complete **CI_CD pipeline with GitHub Actions** with Multistage build configured.


---
**##Project Steps Highlights:**

-Phase1: Creation of Static Web page using HTML and Flask and Containerize using Docker.

-Phase2: CI-CD pipeline with Multistage Build using GitHub Actions.

-Phase3: Kubernetes Deployment on Minikube Cluster(Inside AWS EC2 Instance).

-Phase4: Expose the App via Nginx Reverse Proxy for Public using AWS EC2 Public IP.
 
---

##  Project Tree Structure Details:

```bash
hello-k8s-app/
├── app.py                 # Static Web page on HTML using Flask Framework. 
├── requirements.txt      # Adding Python Flask Dependencies.
├── Dockerfile            # Dockerfile for Containerizing the App on Docker.
├── k8s/
│   ├── deployment.yaml   # Kubernetes Deployment Yaml file.
│   └── service.yaml      # Kubernetes Service Yaml file for Exposing Deployment on NodePort.
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # CI-CD yml file for GitHub Actions Workflow.
├── README.md             # Readme file for Understanding complete architecture of Deployment process.
```

---

## App Description

This Web application displays a simple HTML page with:
-A Header in Blue Background and White bold text on it.
-A Centered body with content, Hello World this is Manu Kumar Message from Minkube!
-A footer with blue background with text: App by Manu Kumar.

---

**Project Creation Explanation:**


-Phase1: Creation of Static Web page using HTML and Flask and Containerize using Docker.
 - 
  The idea is to create a Static web page serving on Docker Container deployed inside Kubernetes Cluster and Exposing to Public access on AWS EC2 instance .

  Step1: Create AWS EC2 instance with t2.large instance size Configuration and SSH to EC2 .

    ```bash
      ssh -i "<PemPrivateKey>.pem" ubuntu@ec2-<ip-address>.eu-west-1.compute.amazonaws.com
   ```

  -Upgrade the EC2 Ubuntu Instance to latest version, create a Directory named hello-k8s-app.

     ```bash
       mkdir hello-k8s-app
    ```
  -add app.py file and enter the contents as it is from the above GitHub file,(or You Clone this Git Repository to get complete code on your local repo)

  -Flask app.py which serves HTML content within its renderning page function created and run locally to see the application with Header and Body and Footer html content.
  
  -Contains Flask as Dependency requirement inside requirement.txt for the application.
   

 Step2: Docker file creation to create a Docker Container image to run app on Minikube cluster
     -Below are the Contents of Dockerfile,
   ```bash
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
   ```   
  -Build the Docker Image with the Below command.
```bash
docker build -t hello-world-app .
```

-Step2: CI-CD pipeline with Multistage Build using GitHub Actions.

-To Automate the App Building process and Verification process of the Static application, we used GitHUb Actions to Build Ci-Cd workflow, the Ci-Cd yml file create in the below given address .github/workflows/ci-cd.yml, below are the contents of Pipeline which ensures the application is correct and building process runs with linting and containerizes the application with latest Docker image on every Git Push action configured on main branch.

Below is the Ci-Cd.yml file for static web app:


-Configuring Trigger on Git Push Requets to the main branch.
 -The Workflow pipeline is triggered with every push actions performed and create new build from the recent change done on main branch.

-Below are the explanation for above steps in CI-CD pipeline worflow stages.



```bash
 steps:
    # ✅ Step 1: Checkout the repository
    - name: Checkout code
      uses: actions/checkout@v3

    # ✅ Step 2: Install and run flake8 for linting
    - name: Run flake8 linter
      run: |
        python -m pip install --upgrade pip
        pip install flake8
        flake8 app.py

    # ✅ Step 3: Set up Docker
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    # ✅ Step 4: Build the Docker image
    - name: Build Docker image
      run: |
        docker build -t hello-world-app .

    # ✅ Step 5: Save the Docker image to a local tarball
    - name: Save Docker image to tar file
      run: |
        mkdir -p docker-output
        docker save hello-world-app -o docker-output/hello-world-app.tar

    # ✅ Step 6: Upload the tarball as a GitHub artifact
    - name: Upload Docker image tarball
      uses: actions/upload-artifact@v4
      with:
        name: docker-image
        path: docker-output/hello-world-app.tar
```
-Step1: Checkout application code from repository.

-Step2: Installs and Runs Flake8 for Liniting and Cheking the code format.

-Step3: Set up Docker for Building Docker images on the local machine using Dockerfile.

-Step4:Building of Hello-world Docker image using the Docker build command.

-Step5:Docker image is Saved in tar file in the local directory(as suggested not to publish in Docker Hub).

-Step6:Upload the tart ball into github Artifact to access every newly built latest image and retrive them when needed.


-Phase3: Kubernetes Deployment on Minikube Cluster(Inside AWS EC2 Instance).

-this phase explaining how we installed and Configured Minikube on EC2 Instanc2(t2.large), Built Docker image inside Minikube, Deployed application using Kubernetes Manifests like Deployment yaml and service Yaml and Cross checked pod and service are running correctly.

-Step 1: Installing MiniKube and Kubectl on EC2.(installig Docker and Kubectl, Minikube with Bash)

-Docker Install:

sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker

-Kubectl Install:

curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

-Minikube Install:

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

Step2:Start the MiniKube with Docker Driver:

minikube start --driver=docker

Check Status of Minikube:

minikube status


Step3: Ensure Minikube uses Docker Daemon for running application,Confirming Docker image is visible inside Minikube cluster:

eval $(minikube docker-env)

Step4: build the Docker image inside Minikube with Existing Dockerfile:

docker build -t hello-world-app .

Step5: Create Kuberenets Manifests files (Deployment and Service YAML files):

-Inside k8s directory create Deployment.yaml and service.yaml files add the below contents:

-inside k8s/deployment.yaml:

apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello
  template:
    metadata:
      labels:
        app: hello
    spec:
      containers:
      - name: hello
        image: hello-world-app
        ports:
        - containerPort: 5000

-Inside k8s/service.yaml:

apiVersion: v1
kind: Service
metadata:
  name: hello-service
spec:
  type: NodePort
  selector:
    app: hello
  ports:
  - port: 80
    targetPort: 5000
    nodePort: 30007

-Step7: appliy Kubernets Manifests file:

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

-Check the status of Kubernets pods and Services:

kubectl get pods
kubectl get svc

-Step8: Check the Minikube Ip and test curl for application output:

minikube ip

curl http://<minikube-ip>:30007


-Step4: Expose the App via Nginx Reverse Proxy for Public using AWS EC2 Public IP.

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

