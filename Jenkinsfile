pipeline {
    agent any

    environment {
        // Nome dell'immagine che creeremo
        IMAGE_NAME = "sentiment-analyzer"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    // Costruisce la nuova immagine sovrascrivendo la vecchia
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo '🧪 Testing...'
                    // Lancia un container di test
                    // Nota: Usiamo --network per far parlare Jenkins col container usando il nome DNS
                    sh "docker run -d --name test-model --network sentiment-analysis_devops-network ${IMAGE_NAME}:latest"
                    sleep 10 
                    
                    // Verifica che risponda su /metrics (più sicuro di /health)
                    // Nota: "test-model" è il nome del container, 5000 è la porta interna
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
                    echo 'Deploying to Production...'
                    // Ferma il container di produzione attuale
                    sh "docker stop production-model || true"
                    sh "docker rm production-model || true"
                    
                    // Avvia quello nuovo
                    // Nota: usiamo --network per ricollegarlo a prometheus
                    sh "docker run -d -p 5000:5000 --name production-model --network sentiment-analysis_monitoring ${IMAGE_NAME}:latest"
                }
            }
        }
    }
}