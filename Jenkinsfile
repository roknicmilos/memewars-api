pipeline {
    agent any
    stages {
        stage("Test") {
            steps {
                sh "sh scripts/pipeline/test.sh"
            }
        }
        stage("STAGING Deploy") {
            when {
                branch 'staging'
            }
            steps {
                sh "sh scripts/pipeline/deploy_staging.sh"
            }
        }
        stage("PRODUCTION Deploy") {
            when {
                branch 'main'
            }
            steps {
                sh "sh scripts/pipeline/deploy_production.sh"
            }
        }
    }
    post {
        success{
            setBuildStatus("Build succeeded", "SUCCESS");
        }
        failure {
            setBuildStatus("Build failed", "FAILURE");
        }
    }
}

void setBuildStatus(String message, String state) {
    step([
        $class: "GitHubCommitStatusSetter",
        reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/roknicmilos/memewars-api"],
        contextSource: [$class: "ManuallyEnteredCommitContextSource", context: "ci/jenkins/build-status"],
        errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
        statusResultSource: [$class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", message: message, state: state]]]
    ]);
}
