
pipeline {
    agent any
    environment {
        IMAGE_NAME = "insecure-blog:${BUILD_NUMBER}"
    }
    stages {
        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }
        stage('Test') {
            steps {
                sh 'pytest tests || true'
            }
        }
        stage('Code Quality') {
            steps {
                withSonarQubeEnv('MySonarQubeServer') {
                    sh "${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=flask_insecure_blog \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_AUTH_TOKEN"
                }
            }
        }
        stage('Security') {
            steps {
                sh 'bandit -r app -f json -o bandit_report.json || true'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
        stage('Release') {
            steps {
                sh './release.sh'
            }
        }
        stage('Monitoring') {
            steps {
                sh 'curl -X POST -H "Content-Type: application/json" -d '{"text": "App deployed in PROD"}' http://localhost:5000/health'
            }
        }
    }
}
