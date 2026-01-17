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
                    echo 'Running Quick Test...'
                    // Avvia un container di test temporaneo
                    sh "docker run -d -p 5001:5000 --name test-model ${IMAGE_NAME}:latest"
                    sleep 10 // Aspetta che parta
                    
                    // Controlla se risponde (se fallisce, la pipeline si ferma)
                    sh "curl --fail http://localhost:5001/metrics || exit 1"
                }
            }
            post {
                always {
                    // Rimuovi il container di test comunque vada
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