pipeline {
  agent any

  environment {
    FRONTEND_DIR = 'frontend'
    BACKEND_DIR = 'backend'
    DOCKER_REGISTRY = 'ahmedhoucine0'
    IMAGE_TAG = "${BUILD_NUMBER}"
  }

  stages {

    stage('Clone Repo') {
      steps {
        git 'https://github.com/ahmedhoucine/AI-consulting-app'
      }
    }

    stage('Install Frontend Dependencies') {
      steps {
        dir("${FRONTEND_DIR}") {
          sh 'npm install'
        }
      }
    }

    stage('Lint & Build Frontend') {
      steps {
        dir("${FRONTEND_DIR}") {
          sh 'npm run lint'
          sh 'npm run build'
        }
      }
    }

    stage('Test Backend') {
      steps {
        dir("${BACKEND_DIR}") {
          sh 'pip install -r requirements.txt'
        }
      }
    }

    stage('Build Docker Images') {
      steps {
        sh "docker build -t $DOCKER_REGISTRY/frontend:$IMAGE_TAG -f Dockerfile.frontend ."
        sh "docker build -t $DOCKER_REGISTRY/backend:$IMAGE_TAG -f Dockerfile.backend ."
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'ahmedhoucine0-dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
          sh 'echo $PASSWORD | docker login -u $USERNAME --password-stdin'
          sh "docker push $DOCKER_REGISTRY/frontend:$IMAGE_TAG"
          sh "docker push $DOCKER_REGISTRY/backend:$IMAGE_TAG"
        }
      }
    }

    
  }

  post {
    failure {
      mail to: 'you@example.com',
           subject: "❌ Build Failed #${BUILD_NUMBER}",
           body: "Check Jenkins for more info."
    }
  }
}
