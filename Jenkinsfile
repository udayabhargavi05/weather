pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        IMAGE_NAME = 'udaya893/weather-forecast:latest'
    }

    stages {
        stage('Checkout GitHub') {
            steps {
                echo 'Pulling Weather Forecasting source code'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Weather Forecasting Docker image'
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Docker Login and Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: udaya983,
                        passwordVariable: Chinnu@2005
                    )
                ]) {
                    bat '''
                        @echo off
                        echo %DOCKER_TOKEN%| docker login -u %DOCKER_USER% --password-stdin
                        if errorlevel 1 exit /b 1
                        docker push %IMAGE_NAME%
                        if errorlevel 1 exit /b 1
                        docker logout
                    '''
                }
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
            echo 'Weather Forecasting CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
