pipeline {
    agent any

    environment {
        // Nome dell'immagine che creeremo
        IMAGE_NAME = "sentiment-analyzer"
        // Nome della rete condivisa definita nel docker-compose
        NETWORK_NAME = "monitoring-network" 
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

        stage('Unit Tests') {
            steps {
                script {
                    echo '🧪 Running Unit Tests...'
                    // Lancia un container temporaneo per eseguire i test con pytest
                    // Installiamo pytest al volo perché potrebbe non essere nell'immagine base se non rebuilding
                    // Oppure assumiamo che Requirements sia stato aggiornato e rebuildato nello step precedente
                    sh "docker run --rm ${IMAGE_NAME}:latest /bin/sh -c 'pip install pytest && pytest test_app.py'"
                }
            }
        }

        stage('Integration Test') {
            steps {
                script {
                    echo '🔗 Running Integration Tests...'
                    // Lancia un container di test collegato alla rete di monitoraggio
                    sh "docker run -d --name test-model --network ${NETWORK_NAME} ${IMAGE_NAME}:latest"
                    sleep 10 
                    
                    // Verifica che risponda su /metrics
                    // Nota: "test-model" è il nome del container
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
                    // Ferma il container di produzione attuale
                    sh "docker stop production-model || true"
                    sh "docker rm production-model || true"
                    
                    // Avvia quello nuovo sulla rete corretta
                    sh "docker run -d -p 5000:5000 --name production-model --network ${NETWORK_NAME} ${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completata con successo! Il modello è in produzione.'
        }
        failure {
            echo '❌ Pipeline fallita. Controlla i log per dettagli.'
        }
    }
}