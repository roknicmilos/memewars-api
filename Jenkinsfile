pipeline {
    agent any
    stages {
        stage("Env vars") {
            steps {
                echo "Start:"
                sh "printenv"
                echo "End"
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
