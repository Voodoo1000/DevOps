pipeline {
    agent any
    environment {
        DOCKERHUB_USERNAME = credentials('dockerhub-username')
        FRONTEND_IMAGE = "voodoo332/devops-frontend"
        BACKEND_IMAGE  = "voodoo332/devops-backend"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push Docker Images') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-username',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )]) {
                        bat '''
                            echo %DOCKER_TOKEN% | docker login -u %DOCKER_USER% --password-stdin
                            docker build -f Dockerfile.frontend -t %FRONTEND_IMAGE%:latest .
                            docker push %FRONTEND_IMAGE%:latest
                            docker build -f Dockerfile.backend -t %BACKEND_IMAGE%:latest .
                            docker push %BACKEND_IMAGE%:latest
                        '''
                    }
                }
            }
        }

        stage('Run Django Tests in Container') {
            steps {
                bat '''
                    docker run -d --name test-backend ^
                      -e DEBUG=True ^
                      -e ALLOWED_HOSTS=* ^
                      voodoo1000/devops-backend:latest ^
                      python manage.py runserver 0.0.0.0:8000
                    timeout /t 10 /nobreak >nul
                    docker exec test-backend python manage.py test
                    docker stop test-backend
                    docker rm test-backend
                '''
            }
        }

        stage('Deploy to Production (main branch)') {
            when { branch 'main' }
            steps {
                echo "Образы готовы к деплою!"
            }
        }
    }
    post {
        always {
            bat "docker logout || exit 0"
        }
    }
}

// pipeline {
//     agent any

//     environment {
//         EMAIL_RECIPIENT = 'vlad.butakov.2004@mail.ru'
//         VUE_DIR = 'client'
//         DJANGO_DIR = '.'
//     }

//     stages {
//         stage('Debug Branch Info') {
//             steps {
//                 script {
//                     echo "GIT_BRANCH: '${env.GIT_BRANCH}'"
//                 }
//             }
//         }

//         stage('Checkout') {
//             steps {
//                 echo 'Cloning repository...'
//                 checkout scm
//             }
//         }

//         stage('Install Python Dependencies') {
//             steps {
//                 echo 'Installing Python dependencies (Django)...'
//                 bat "pip install -r ${DJANGO_DIR}/requirements.txt"
//             }
//         }

//         stage('Install Node.js Dependencies (Vue)') {
//             when {
//                 anyOf {
//                     changeRequest() 
//                     expression { return env.GIT_BRANCH == 'origin/dev' }
//                     expression { return env.GIT_BRANCH == 'origin/main' }
//                     expression { env.GIT_BRANCH?.startsWith('origin/fix/') }
//                 }
//             }
//             steps {
//                 echo 'Installing Node.js dependencies (Vue frontend)...'
//                 bat "cd ${VUE_DIR} && npm install"
//             }
//         }

//         stage('Build Vue.js Frontend') {
//             when {
//                 anyOf {
//                     changeRequest() 
//                     expression { return env.GIT_BRANCH == 'origin/dev' }
//                     expression { return env.GIT_BRANCH == 'origin/main' }
//                     expression { env.GIT_BRANCH?.startsWith('origin/fix/') }
//                 }
//             }
//             steps {
//                 echo 'Building Vue.js application...'
//                 bat "cd ${VUE_DIR} && npm run build"

//                 bat "if not exist \"${DJANGO_DIR}\\static\\frontend\" mkdir \"${DJANGO_DIR}\\static\\frontend\""
//                 bat "xcopy /E /I /Y \"${VUE_DIR}\\dist\\*\" \"${DJANGO_DIR}\\static\\frontend\\\""

//                 echo 'Vue.js built and copied to Django static/frontend folder.'
//             }
//         }

//         stage('Run Django Tests') {
//             when {
//                 anyOf {
//                     changeRequest() 
//                     expression { return env.GIT_BRANCH == 'origin/dev' }
//                     expression { return env.GIT_BRANCH == 'origin/main' }
//                     expression { env.GIT_BRANCH?.startsWith('origin/fix/') }
//                 }
//             }
//             steps {
//                 echo 'Running Django tests...'
//                 bat "python ${DJANGO_DIR}/manage.py test --verbosity=2"
//             }
//             post {
//                 failure {
//                     emailext(
//                         subject: "TEST FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
//                         body: """<h3>Django/Vue CI Failed!</h3>
//                                  <p><strong>Branch:</strong> ${env.GIT_BRANCH}</p>
//                                  <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
//                                  <p><strong>Log:</strong> <a href="${env.BUILD_URL}console">View Console</a></p>""",
//                         to: "${env.EMAIL_RECIPIENT}",
//                         recipientProviders: [[$class: 'DevelopersRecipientProvider']]
//                     )
//                 }
//             }
//         }

//         stage('Deploy to Production (main branch)') {
//             when {
//                 expression { return env.GIT_BRANCH == 'origin/main'}
//             }
//             steps {
//                 echo 'Deploying to production...'

//                 bat "cd ${VUE_DIR} && npm run build"

//                 bat "if not exist \"${DJANGO_DIR}\\static\\frontend\" mkdir \"${DJANGO_DIR}\\static\\frontend\""
//                 bat "xcopy /E /I /Y \"${VUE_DIR}\\dist\\*\" \"${DJANGO_DIR}\\static\\frontend\\\""

//                 bat "echo Deployment successful at %DATE% %TIME% on branch main > deployment.log"
//                 bat "echo Git commit: %GIT_COMMIT% >> deployment.log"

//                 archiveArtifacts artifacts: 'deployment.log', allowEmptyArchive: true

//                 echo 'Production deploy prepared!'
//             }
//             post {
//                 success {
//                     emailext(
//                         subject: "DEPLOYED TO PRODUCTION: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
//                         body: """<h2>Production Deployment Prepared!</h2>
//                                  <p><strong>Project:</strong> Django + Vue.js</p>
//                                  <p><strong>Branch:</strong> ${env.GIT_BRANCH}</p>
//                                  <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
//                                  <p><strong>Deployment log attached.</strong></p>
//                                  <p><a href="${env.BUILD_URL}">View Build</a></p>""",
//                         to: "${env.EMAIL_RECIPIENT}"
//                     )
//                 }
//             }
//         }
//     }

//     post {
//         always {
//             echo 'Cleaning workspace...'
//             cleanWs()
//         }
//         failure {
//             emailext(
//                 subject: "BUILD FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
//                 body: """<h3>Build failed during pipeline execution.</h3>
//                          <p>Check logs: <a href="${env.BUILD_URL}console">Console Output</a></p>""",
//                 to: "${env.EMAIL_RECIPIENT}"
//             )
//         }
//     }