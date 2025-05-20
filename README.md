**###Hello All, This is a Explanation of Project for Hosting Static Web App on MiniKube inside AWS EC2 with NGINX Reverse Proxy.**
 
**##Access application on URL:** http://52.16.78.143

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
 
  ```bash
   from flask import Flask #import Flask 


app = Flask(__name__)


@app.route('/')
def home():
    return '''  #returning HTML wenpage as output.
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello World</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background-color: #f8f8f8;
                color: #333;
            }
            header, footer {
                background-color: #004080;
                color: white;
                text-align: center;
                padding: 20px;
            }
            main {
                padding: 40px;
                text-align: center;
            }
            h1 {
                font-weight: bold;
                color: #004080;
            }
        </style>
    </head>
    <body>
        <header>
            <h2> My Static Web Page using Falsk and Kubernetes</h2> #header Description
        </header>
        <main>
            <h1>Hello, World from <strong>Kubernetes</strong>!</h1>
            <p>This is a static-style page served by Flask in a container.</p> #Body Description of Static Web page.
        </main>
        <footer>
            <p>App Created by Manu Kumar</p>#Footer Description
        </footer>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  #Run the Application on port 5000
  ```
  -Flask app.py which serves HTML content within its renderning page function created and run locally to see the application with Header and Body and Footer html content.
  
  -Contains Flask as Dependency requirement inside requirement.txt for the application.
   

 Step2: Docker file creation to create a Docker Container image to run app on Minikube cluster
     -Below are the Contents of Dockerfile,
   ```bash
FROM python:3.9-slim #Use Python officila image for Conatiner Creation.
WORKDIR /app  #Set Workdirectory.
COPY requirements.txt . #Copy Requirements file to create docker container using flask requirement.
RUN pip install -r requirements.txt #run flask requirement command
COPY . . #copy all the source code present work directory of container.
EXPOSE 5000  #Expose the container to 5000
CMD ["python", "app.py"] #execute Command python and app.py 
   ```    
  -Build the Docker Image with the Below command.
```bash
docker build -t hello-world-app . #Docker Buid Command to create Docker image
```

**-Phase2: CI-CD pipeline with Multistage Build using GitHub Actions.**

-To Automate the App Building process and Verification process of the Static application, I used GitHUb Actions to Build Ci-Cd workflow, the Ci-Cd yml file create in the below given address .github/workflows/ci-cd.yml, below are the contents of Pipeline which ensures the application is correct and building process runs with linting and containerizes the application with latest Docker image on every Git Push action configured on main branch.

Below is the Ci-Cd.yml file for static web app:


-Configuring Trigger on Git Push Requets to the main branch.
 -The Workflow pipeline is triggered with every push actions performed and create new build from the recent change done on main branch.

-Below are the explanation for above steps in CI-CD pipeline worflow stages.



```bash
name: CI/CD Pipeline  #name of the Pipeline

on:
  push:   #trigger created for all the Git Push confirmed on Main branch.
    branches:
      - main
  pull_request:

jobs:
  build:   #runs the job on Ubuntu Server 
    runs-on: ubuntu-latest

    steps:
    #  Step 1: Checkout the Git Main branch repository 
    - name: Checkout code
      uses: actions/checkout@v3

    # Step 2: Install and run flake8 for linting for format and error detection.
    - name: Run flake8 linter
      run: |
        python -m pip install --upgrade pip
        pip install flake8
        flake8 app.py

    # Step 3: Set up Docker to create image of Platform independent.
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    # Step 4: Build the Docker image for creating Docker Container.
    - name: Build Docker image
      run: |
        docker build -t hello-world-app .

    # Step 5: Save the Docker image to a local tarball (As suggested in the task not to store in DokcerHUb)
    - name: Save Docker image to tar file
      run: |
        mkdir -p docker-output
        docker save hello-world-app -o docker-output/hello-world-app.tar

    # Step 6: Upload the tarball as a GitHub artifact, for every sucessfull build workflow docker latest image is created.
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

-Step5:Docker image is Saved as tar file in the GitHub Artifact directory(as suggested not to publish in Docker Hub).

-Step6:Upload the tar file into github Artifact to access every newly built latest image and retrive them when needed.


**-Phase3: Kubernetes Deployment on Minikube Cluster(Inside AWS EC2 Instance).**

-this phase explaining how we installed and Configured Minikube on EC2 Instanc2(t2.large), Built Docker image inside Minikube, Deployed application using Kubernetes Manifests like Deployment yaml and service Yaml and Cross checked pod and service are running correctly.

-Step 1: Installing MiniKube and Kubectl on EC2.(installig Docker and Kubectl, Minikube with Bash)

-Docker Install:

```bash
sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
```

-Kubectl Install:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

-Minikube Install: #Minikube install commands

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Step2:Start the MiniKube with Docker Driver:

```bash
minikube start --driver=docker  #starting Minikube using Docker as Driver
```

Check Status of Minikube:

```bash
minikube status  #Checking the Status of minikube for running pods inside it.
```

Step3: Ensure Minikube uses Docker Daemon for running application,Confirming Docker image is visible inside Minikube cluster:

```bash
eval $(minikube docker-env)  #setting Docker environment inside minikube
```

Step4: build the Docker image inside Minikube with Existing Dockerfile:

```bash
docker build -t hello-world-app .  #Docker Build for creating container image
```

Step5: Create Kuberenets Manifests files (Deployment and Service YAML files):

-Inside k8s directory create Deployment.yaml and service.yaml files add the below contents:

-inside k8s/deployment.yaml:

```bash
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
```

-Inside k8s/service.yaml:

```bash
apiVersion: v1
kind: Service
metadata:
  name: hello-service
spec:
  type: NodePort   #nodeport type is used for expose single pod to stable network endpoint to outside.
  selector:
    app: hello
  ports:
  - port: 80
    targetPort: 5000
    nodePort: 30007
```

-Step7: appliy Kubernets Manifests file:

```bash
kubectl apply -f k8s/deployment.yaml. #manuall Application Deployment through manifest files
kubectl apply -f k8s/service.yaml
```

-Check the status of Kubernets pods and Services:

```bash
kubectl get pods #Checking pods state 
kubectl get svc  #checking service for Nodeport service expose
```

-Step8: Check the Minikube Ip and test curl for application output:

```bash
minikube ip
curl http://<minikube-ip>:30007
```

**-Phase4: Expose the App via Nginx Reverse Proxy for Public Access using AWS EC2 Public IP.**

-Once the app is deployed on Minikube, its accessible internally via Minikube's IP and NodePort Service, but it does not available publically on any browser and with the EC2 public IP address , so i need a tunnel service or reverse Proxy or Loadbalancer to host publicly on Internet,i choosed Nginx as a Reverse proxy inside EC2 instance.

-below are the steps to configure and access static web app on EC2 public IP.

-Step1: Installing NGINX service on EC2:

```bash
sudo apt update
sudo apt install nginx -y

```

-Step2: Get Minikube IP and NodePort Service Address:

```bash
minikube ip  #Minikube IP
kubectl get svc #Service Address as Nodeport
```

-Step3:Configuring NGINX Reverse Proxy, Edit the Nginx Config file:

```bash
sudo nano /etc/nginx/sites-available/default  #edit the nginx Config file
```

```bash
server {
    listen 80 default_server;  #http response listens to server ip on application layer
    listen [::]:80 default_server;

    server_name _;

    location / {
        proxy_pass http://<MINIKUBE_IP>:30007;  # Minikube Ip is served to public IP of EC2 for Public acccess of EC2.
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

-step4:Save and Test the nginx configuration file and Restart the service:

```bash
sudo nginx -t
sudo systemctl restart nginx  #restart the Nginx service
```

-Step5: Application Access on Public EC2 Ip address:
```bash
http://52.16.78.143  #Elastic IP is Associated to EC2 Server
#Access the application live and view the static content on EC2 server IP address.

```
