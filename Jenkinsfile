pipeline {
    agent any
    stages {
        stage("Test") {
            steps {
                sh "sh scripts/pipeline/test.sh"
            }
        }
        stage("Staging Deploy") {
            when {
                branch 'staging'
            }
            steps {
                sh "sh scripts/pipeline/deploy_staging.sh"
            }
        }
    }
}
