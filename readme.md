

jenkins setup:

plugins:

 Git

 Docker Pipeline

 NodeJS

 Pipeline

 SSH Agent (for server deployment)

 Blue Ocean (optional UI improvement)

 add nodejs tool
 add dockerhub credantials

 backend pipeline:

 pipeline {
  agent any
  environment {
    BACKEND_DIR = 'backend'
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

    stage('Build Backend Docker Image') {
      steps {
        sh "docker build -t $DOCKER_REGISTRY/backend:$IMAGE_TAG -f Dockerfile.backend ."
      }
    }

    stage('Push Backend Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'ahmedhoucine0-dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
          sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
          sh "docker push $DOCKER_REGISTRY/backend:$IMAGE_TAG"
        }
      }
    }
  }
  post {
    failure {
      mail to: 'ahcine00@gmail.com',
           subject: "❌ Backend Build Failed #${BUILD_NUMBER}",
           body: "Check Jenkins for more info."
    }
  }
}



frontend pipeline:

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
