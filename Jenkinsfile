pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/kayoulou/Voting-app.git'
        REPO_BRANCH = 'main'
        ENV_FILE = '.env'
    }

    stages {
        stage('Clone') {
            steps {
                echo "===> Clonage du dépôt ${REPO_URL} sur la branche ${REPO_BRANCH}"
                git url: "${REPO_URL}", branch: "${REPO_BRANCH}"
            }
        }

        stage('Build') {
            steps {
                echo "===> Construction des images Docker"
                sh 'docker compose --env-file ${ENV_FILE} build'
            }
        }

        stage('Deploy') {
            steps {
                echo "===> Arrêt et suppression des anciens containers"
                sh 'docker compose --env-file ${ENV_FILE} down -v'
                echo "===> Déploiement des nouveaux containers"
                sh 'docker compose --env-file ${ENV_FILE} up -d'
            }
        }
    }

    post {
        always {
            echo "===> État actuel des containers"
            sh 'docker compose ps'
        }
        success {
            echo "✅ Pipeline exécutée avec succès !"
        }
        failure {
            echo "❌ La pipeline a échoué."
        }
    }
}
