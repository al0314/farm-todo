pipeline {
    agent { label 'master'}
    environment {
        DOCKER_IMAGE = "al0314/farm-todo"
        IMAGE_TAG = "${GIT_TAG_NAME}" // This was extracted from the webhook JSON
  }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: 'centos_ida_rsa', url: 'https://github.com/al0314/farm-todo'
            }
        }
        
        stage('Run') {
            steps {
                sh 'ls -l' // or 'dir' on Windows
                sh 'scp -r . vagrant@192.168.56.11:/var/lib/jenkins'
            }
        }
        
        
        
        
        stage('Test') {
            agent { label 'test'}
            steps {
                sh ' scp -r vagrant@192.168.10.111:/var/lib/jenkins/workspace/farm-todo /opt/jenkins '
                sh ' cd /opt/jenkins/farm-todo '
                sh ' docker compose up -d --build '
                sh ' docker exec -it farm-todo-backend '
                sh ' pytest ./src/tests/ '
            }
        }
        stage ('Build image') {
            steps {
                sh """
                echo "Building docker image....."
                docker build -t al0314/farm-todo:${env.IMAGE_TAG} .
                """
            }
        }
        
        stage ('push image') {
            steps {
                sh "docker push al0314/farm-todo:${env.IMAGE_TAG}"
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'ls -l' // or 'dir' on Windows
            }
        }

        
    }
}
