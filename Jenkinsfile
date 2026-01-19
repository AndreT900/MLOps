pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        IMAGE_NAME = "sentiment-analyzer"
        NETWORK_NAME = "monitoring-network" 
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    echo '🧪 Running Unit Tests...'
                    sh "docker run --rm ${IMAGE_NAME}:latest /bin/sh -c 'pip install pytest && pytest test_app.py'"
                }
            }
        }

        stage('Integration Test') {
            steps {
                script {
                    echo '🔗 Running Integration Tests...'
                    sh "docker run -d --name test-model --network ${NETWORK_NAME} ${IMAGE_NAME}:latest"
                    sleep 10 
                    sh "curl --fail http://test-model:5000/metrics"
                }
            }
            post {
                always {
                    sh "docker rm -f test-model"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo '🚀 Deploying to Production...'
                    sh "docker stop production-model || true"
                    sh "docker rm production-model || true"
                    sh "docker run -d -p 5000:5000 --name production-model --network ${NETWORK_NAME} ${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completata con successo! Il modello è in produzione.'
        }
        failure {
            echo 'Pipeline fallita. Controlla i log per dettagli.'
        }
    }
}