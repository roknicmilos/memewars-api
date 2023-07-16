pipeline {
    agent any
    stages {
        stage("Staging Deploy") {
            when {
                branch 'staging'
            }
            steps {
                sh "sh scripts/deploy_staging.sh"
            }
        }
        stage("Test") {
            steps {
                echo "Current directory: $PWD"
                echo "Content of the current directory:"
                sh "ls -la"
                sh "cp example.env .env"
                sh "docker compose -f docker-compose.test.yml build --no-cache"
                sh "docker compose -f docker-compose.test.yml run --rm django"
                sh "docker compose down"
            }
        }
    }
}
