pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "al0314/farm-todo"
        IMAGE_TAG = "${GIT_TAG_NAME}" // This was extracted from the webhook JSON
  }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: 'github-creds', url: 'https://github.com/al0314/flask-docker-starterkit.git'
            }
        }
        
        stage('Run') {
            steps {
                sh 'ls -l' // or 'dir' on Windows
            }
        }
        stage ('Build image') {
            steps {
                sh """
                echo "Building docker image....."
                docker build -t al0314/flask-docker-starterkit:${env.IMAGE_TAG} .
                """
            }
        }
        
        
        
        stage('Test') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
                sh './venv/bin/pip install pytest'
                sh ''' 
                    export PYTHONPATH=$(pwd)
                    ./venv/bin/pytest ./flask_starterkit/tests/
                '''
            }
        }
        
        stage ('push image') {
            steps {
                sh "docker push al0314/flask-docker-starterkit:${env.IMAGE_TAG}"
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'ls -l' // or 'dir' on Windows
            }
        }

        
    }
}
