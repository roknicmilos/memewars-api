def setGitHubStatus(status, message) {
// Get the GitHub server configuration.
def githubServer = Jenkins.instance.getDescriptorByType(org.jenkinsci.plugins.github.webhook.GitHubServer.class)

// Set the GitHub status.
githubServer.setBuildStatus(status, message, context.build.getUrl())
}

pipeline {
    agent any
    stages {
        stage("Test") {
            steps {
                sh "sh scripts/pipeline/test.sh"
                setGitHubStatus('Success', 'All tests passed.')
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
}
