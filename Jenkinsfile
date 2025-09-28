pipeline {
    agent any

    environment {
        EMAIL_RECIPIENT = 'vlad.butakov.2004@mail.ru'
        VUE_DIR = 'client'
        DJANGO_DIR = '.'
    }

    stages {
        stage('Debug Branch Info') {
            steps {
                script {
                    echo "GIT_BRANCH: '${env.GIT_BRANCH}'"
                }
            }
        }

        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Install Python Dependencies') {
            steps {
                echo 'Installing Python dependencies (Django)...'
                bat "pip install -r ${DJANGO_DIR}/requirements.txt"
            }
        }

        stage('Install Node.js Dependencies (Vue)') {
            when {
                anyOf {
                    changeRequest() 
                    expression { return env.GIT_BRANCH == 'origin/dev' }
                    expression { return env.GIT_BRANCH == 'origin/main' }
            }
            steps {
                echo 'Installing Node.js dependencies (Vue frontend)...'
                bat "cd ${VUE_DIR} && npm install"
            }
        }

        stage('Build Vue.js Frontend') {
            when {
                anyOf {
                    changeRequest() 
                    expression { return env.GIT_BRANCH == 'origin/dev' }
                    expression { return env.GIT_BRANCH == 'origin/main' }
            }
            steps {
                echo 'Building Vue.js application...'
                bat "cd ${VUE_DIR} && npm run build"

                bat "if not exist \"${DJANGO_DIR}\\static\\frontend\" mkdir \"${DJANGO_DIR}\\static\\frontend\""
                bat "xcopy /E /I /Y \"${VUE_DIR}\\dist\\*\" \"${DJANGO_DIR}\\static\\frontend\\\""

                echo 'Vue.js built and copied to Django static/frontend folder.'
            }
        }

        stage('Run Django Tests') {
            when {
                anyOf {
                    changeRequest() 
                    expression { return env.GIT_BRANCH == 'origin/dev' }
                    expression { return env.GIT_BRANCH == 'origin/main' }
            }
            steps {
                echo 'Running Django tests...'
                bat "python ${DJANGO_DIR}/manage.py test --verbosity=2"
            }
            post {
                failure {
                    emailext(
                        subject: "TEST FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """<h3>Django/Vue CI Failed!</h3>
                                 <p><strong>Branch:</strong> ${env.GIT_BRANCH}</p>
                                 <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
                                 <p><strong>Log:</strong> <a href="${env.BUILD_URL}console">View Console</a></p>""",
                        to: "${env.EMAIL_RECIPIENT}",
                        recipientProviders: [[$class: 'DevelopersRecipientProvider']]
                    )
                }
            }
        }

        stage('Deploy to Production (main branch)') {
            when {
                expression { return env.GIT_BRANCH == 'origin/main'}
            }
            steps {
                echo 'Deploying to production...'

                bat "cd ${VUE_DIR} && npm run build"

                bat "if not exist \"${DJANGO_DIR}\\static\\frontend\" mkdir \"${DJANGO_DIR}\\static\\frontend\""
                bat "xcopy /E /I /Y \"${VUE_DIR}\\dist\\*\" \"${DJANGO_DIR}\\static\\frontend\\\""

                bat "echo Deployment successful at %DATE% %TIME% on branch main > deployment.log"
                bat "echo Git commit: %GIT_COMMIT% >> deployment.log"

                archiveArtifacts artifacts: 'deployment.log', allowEmptyArchive: true

                echo 'Production deploy prepared!'
            }
            post {
                success {
                    emailext(
                        subject: "DEPLOYED TO PRODUCTION: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """<h2>Production Deployment Prepared!</h2>
                                 <p><strong>Project:</strong> Django + Vue.js</p>
                                 <p><strong>Branch:</strong> ${env.GIT_BRANCH}</p>
                                 <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
                                 <p><strong>Deployment log attached.</strong></p>
                                 <p><a href="${env.BUILD_URL}">View Build</a></p>""",
                        to: "${env.EMAIL_RECIPIENT}"
                    )
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning workspace...'
            cleanWs()
        }
        failure {
            emailext(
                subject: "BUILD FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """<h3>Build failed during pipeline execution.</h3>
                         <p>Check logs: <a href="${env.BUILD_URL}console">Console Output</a></p>""",
                to: "${env.EMAIL_RECIPIENT}"
            )
        }
    }
}