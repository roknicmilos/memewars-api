pipeline {
    agent any
    stages {
        stage("Build") {
            steps {
                echo "Checking..."
                sh "git --version"
                sh "docker --version"
            }
        }
    }
}
