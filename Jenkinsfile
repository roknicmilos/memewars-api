pipeline {
    agent any
    stages {
        stage("Staging Deploy") {
            when {
                branch 'staging'
            }
            steps {
                sh "cd $MW_API_STAGING_DIR_PATH"
                sh "git fetch origin"
                sh "git reset --hard origin/staging || exit"
                sh "cat .env"
                // sh "docker compose build"
                // sh "docker compose -p memewars-api-staging up -d"
                // sh "docker exec -t memewars-django--staging sh -c 'pytest --create-db --cov -n auto && coverage html'"
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
