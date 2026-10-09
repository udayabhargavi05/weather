pipeline {
    agent any
    stages
    {
        stage('Build Docker Image') {
            steps {
                echo "Build Docker Image"
                bat "docker build -t weather-forecast:latest ."
            }
        }
        stage('Docker Login') {
            steps {
                  bat 'docker login -u udaya893 -p Chinnu@2005'
                }
            }
        stage('push Docker Image to Docker Hub') {
            steps {
                echo "push Docker Image to Docker Hub"
                bat "docker tag weather-forecast:latest udaya893/sample:weather-forecast"               
                    
                bat "docker push udaya893/sample:weather-forecast"
                
            }
        }
       stage('Deploy to Kubernetes') {
    steps {
        bat 'kubectl apply -f k8/deployment.yaml'
        bat 'kubectl apply -f k8/service.yaml'

        bat 'kubectl rollout restart deployment/weather-forecast-deployment'
        bat 'kubectl rollout status deployment/weather-forecast-deployment --timeout=180s'
    }
}
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}