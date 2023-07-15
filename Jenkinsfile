pipeline {
    agent any
    stages {
        stage("Build") {
            steps {
                sh "docker compose run --rm django sh -c 'pytest --cov -n auto'"
            }
        }
    }
}
