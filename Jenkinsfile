pipeline {
    agent none
    environment {
        DOCKER_IMAGE = "al0314/farm-todo"
        IMAGE_TAG = "${GIT_TAG_NAME}" // This was extracted from the webhook JSON
  }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', credentialsId: 'centos_id_rsa', url: 'https://github.com/al0314/farm-todo'
            }
        }
        
        stage('Run') {
            steps {
                sh 'ls -l' // or 'dir' on Windows
            }
        }
        
        
        
        
        stage('Test') {
            agent { label 'test'}
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/activate && pip install -r requirements.txt'
                sh ''' 
                    export PYTHONPATH=$(pwd)
                    ./venv/bin/pytest ./backend/src/tests/
                '''
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
