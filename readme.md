# 🚀 AI Consulting App - CI/CD Pipeline with Jenkins

##  to run the application in microservice mode 
1- run Consul in docker container using port 8500

2- run each microservice 

3- run api gateway

4- run the front application 

## 🐳 Jenkins Setup
```bash
docker run -d --name jenkins --user root  -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home  jenkins/jenkins:lts

  ```

Access at: http://localhost:8080
Initial password:
```bash 
 docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
 ```





# 🔧 plugins:
Git

Docker Pipeline

NodeJS

Pipeline

SSH Agent

Blue Ocean (optional)

# 🔐 Credentials
DockerHub Username & Password
Manage Jenkins > Credentials > Global > Add Credentials

ID: ahmedhoucine0-dockerhub

# ⚙️ Tools Configuration
Go to: Manage Jenkins > Global Tool Configuration

Add NodeJS:

Name: nodejs

Version: (Select latest LTS)



# backend pipeline:
```bash 

pipeline {
  agent any
  environment {
    DOCKER_REGISTRY = 'ahmedhoucine0'
    IMAGE_TAG = "${BUILD_NUMBER}"
    SERVICES = "recommendation_service advisor_service dashboard_service api_gateway"   
  }

  stages {
    stage('Clean Workspace') {
      steps {
        cleanWs()
      }
    }

    stage('Clone Repo') {
      steps {
        git 'https://github.com/ahmedhoucine/AI-consulting-app'
      }
    }

    stage('Detect Changed Services') {
      steps {
        script {
          // Compare with previous commit to detect changes
          CHANGED_SERVICES = sh(
            script: """
              git fetch --all
              git diff --name-only HEAD~1 HEAD | cut -d/ -f1 | sort -u
            """,
            returnStdout: true
          ).trim()

          echo "📂 Changed folders: ${CHANGED_SERVICES}"

          // Intersect with SERVICES list
          BUILD_SERVICES = []
          for (s in SERVICES.split(" ")) {
            if (CHANGED_SERVICES.contains(s)) {
              BUILD_SERVICES << s
            }
          }

          if (BUILD_SERVICES.size() == 0) {
            echo "✅ No microservice changes detected. Skipping build."
            currentBuild.result = 'SUCCESS'
            skipBuild = true
          } else {
            echo "🚀 Services to build: ${BUILD_SERVICES.join(', ')}"
            skipBuild = false
          }
        }
      }
    }

    stage('Build Docker Images') {
      when {
        expression { return !skipBuild }
      }
      steps {
        script {
          for (s in SERVICES.split(" ")) {
                echo "🚀 Building image for ${s}"
                sh "docker build -t $DOCKER_REGISTRY/${s}:${IMAGE_TAG} -f ${s}/Dockerfile ./${s}"
            }
        }
      }
    }

    stage('Push Docker Images') {
      when {
        expression { return !skipBuild }
      }
      steps {
        withCredentials([usernamePassword(credentialsId: 'ahmedhoucine0-dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
          sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
          script {
            for (s in BUILD_SERVICES) {
              echo "📤 Pushing image for ${s}"
              sh "docker push $DOCKER_REGISTRY/${s}:${IMAGE_TAG}"
              sh "docker tag $DOCKER_REGISTRY/${s}:${IMAGE_TAG} $DOCKER_REGISTRY/${s}:latest"
              sh "docker push $DOCKER_REGISTRY/${s}:latest"
            }
          }
        }
      }
    }
  }

  post {
    failure {
      mail to: 'ahcine00@gmail.com',
           subject: "❌ Build Failed #${BUILD_NUMBER}",
           body: "Check Jenkins for more info."
    }
    success {
      mail to: 'ahcine00@gmail.com',
           subject: "✅ Build Success #${BUILD_NUMBER}",
           body: "Successfully built & pushed: ${BUILD_SERVICES}"
    }
  }
}


```


# frontend pipeline:
```bash 
pipeline {
  agent any
  tools {
    nodejs 'nodejs'
  }
  environment {
    FRONTEND_DIR = 'frontend'
    DOCKER_REGISTRY = 'ahmedhoucine0'
    IMAGE_TAG = "${BUILD_NUMBER}"
  }

  stages {
    stage('Clean Workspace') {
      steps {
        cleanWs()
      }
    }

    stage('Clone Repo') {
      steps {
        git 'https://github.com/ahmedhoucine/AI-consulting-app'
      }
    }

    stage('Build and Cache Frontend Dependencies') {
      steps {
        dir("${FRONTEND_DIR}") {
          sh 'npm ci --legacy-peer-deps'
        }
      }
    }

    stage('Build Frontend') {
      steps {
        dir("${FRONTEND_DIR}") {
          sh 'npm run build'
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          sh """
            docker build --pull --no-cache=false -t $DOCKER_REGISTRY/frontend:$IMAGE_TAG -f Dockerfile.frontend .
          """
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'ahmedhoucine0-dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
          sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
          sh "docker push $DOCKER_REGISTRY/frontend:$IMAGE_TAG"
        }
      }
    }
  }

  post {
    failure {
      mail to: 'ahcine00@gmail.com',
           subject: "❌ Build Failed #${BUILD_NUMBER}",
           body: "Check Jenkins for more info."
    }
  }
}
```


 docker run --env-file .env -d -p 5000:5000 --name consulting-backend consulting-backend:latest