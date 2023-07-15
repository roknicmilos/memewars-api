pipeline {
    agent any
    stages {
        stage("Build") {
            steps {
                echo "Current directory: $PWD"
                echo "Content of the current directory:"
                sh "ls -la"
                sh "cp example.env .env"
                sh "docker compose run --rm django sh -c 'pytest -n auto'"
            }
        }
    }
}
