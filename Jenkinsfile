pipeline {
    agent any

    environment {
        EMAIL_RECIPIENT = 'vlad.butakov.2004@mail.ru'
        VUE_DIR = 'client'
        DJANGO_DIR = '.'
    }

    stages {
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
                expression {
                    return env.GIT_BRANCH == 'origin/dev' ||
                           env.GIT_BRANCH == 'origin/fix' ||
                           env.GIT_BRANCH == 'origin/main'
                }
            }
            steps {
                echo 'Installing Node.js dependencies (Vue frontend)...'
                bat "cd ${VUE_DIR} && npm install"
            }
        }

        stage('Build Vue.js Frontend') {
            when {
                expression {
                    return env.GIT_BRANCH == 'origin/dev' ||
                           env.GIT_BRANCH == 'origin/fix' ||
                           env.GIT_BRANCH == 'origin/main'
                }
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
                expression {
                    return env.GIT_BRANCH == 'origin/dev' ||
                           env.GIT_BRANCH == 'origin/fix' ||
                           env.GIT_BRANCH == 'origin/main'
                }
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

        stage('Merge fix to dev') {
            when {
                expression {
                    return env.GIT_BRANCH == 'origin/fix'
                }
            }
            steps {
                script {
                    bat """
                        git config --global user.email "jenkins@localhost"
                        git config --global user.name "Jenkins CI"
                        git checkout dev
                        git pull origin dev
                        git merge --no-ff origin/fix -m "Auto-merge from fix branch"
                        git push origin dev
                    """
                    
                    echo "Successfully merged fix into dev!"
                }
            }
            post {
                failure {
                    emailext(
                        subject: "MERGE FAILED: fix → dev in ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """<h3>Merge from fix to dev failed!</h3>
                                <p><strong>Branch:</strong> ${env.GIT_BRANCH}</p>
                                <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
                                <p><strong>Log:</strong> <a href="${env.BUILD_URL}console">View Console</a></p>""",
                        to: "${env.EMAIL_RECIPIENT}"
                    )
                }
            }
        }

        stage('Deploy to Production (main branch)') {
            when {
                expression {
                    return env.GIT_BRANCH == 'origin/main'
                }
            }
            steps {
                echo 'Deploying to production...'

                // 1. Собираем Vue.js
                bat "cd ${VUE_DIR} && npm run build"

                bat "if not exist \"${DJANGO_DIR}\\static\\frontend\" mkdir \"${DJANGO_DIR}\\static\\frontend\""
                bat "xcopy /E /I /Y \"${VUE_DIR}\\dist\\*\" \"${DJANGO_DIR}\\static\\frontend\\\""

                bat "echo Deployment successful at %DATE% %TIME% on branch main > deployment.log"
                bat "echo Git commit: %GIT_COMMIT% >> deployment.log"
                archiveArtifacts artifacts: 'deployment.log', allowEmptyArchive: true

                echo 'Starting Django server on http://localhost:8000...'
                bat "cd ${DJANGO_DIR}"
                powershell 'start "DjangoServer" cmd /k "python manage.py runserver 8000"' 
                bat 'timeout /t 5 >nul'

                bat "for /F \"tokens=2\" %i in ('tasklist ^| findstr \"python\"') do set PID=%i"
                bat "echo Django server PID: %PID%"
                bat "echo %PID% > django_pid.txt"
                archiveArtifacts artifacts: 'django_pid.txt', allowEmptyArchive: true

                echo 'Django server started on http://localhost:8000 (for demo only)'
            }
            post {
                success {
                    emailext(
                        subject: "DJANGO SERVER DEPLOYED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """<h2>🎉 Django Server Deployed!</h2>
                                <p><strong>Project:</strong> Django + Vue.js</p>
                                <p><strong>Branch:</strong> ${env.GIT_BRANCH}</p>
                                <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
                                <p><strong>Server URL:</strong> <a href="http://localhost:8000">http://localhost:8000</a> (on Jenkins machine)</p>
                                <p><em>Note: This is a demo server. For production, use Gunicorn/Nginx/Docker.</em></p>
                                <p><strong>Deployment log attached.</strong></p>
                                <p><a href="${env.BUILD_URL}">View Build</a></p>""",
                        to: "${env.EMAIL_RECIPIENT}"
                    )
                }
                failure {
                    emailext(
                        subject: "DEPLOY FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                        body: """<h3>🚨 Deployment failed!</h3>
                                <p><strong>Branch:</strong> ${env.GIT_BRANCH}</p>
                                <p><strong>Log:</strong> <a href="${env.BUILD_URL}console">View Console</a></p>""",
                        to: "${env.EMAIL_RECIPIENT}"
                    )
                }
            }
        }
        // stage('Kill Django Server') {
        //     when {
        //         expression { return true } 
        //     }
        //     steps {
        //         echo "Killing Django server process..."
        //         script {
        //             if (fileExists('django_server.pid')) {
        //                 def pid = readFile('django_server.pid').trim()
        //                 try {
        //                     bat "taskkill /PID ${pid} /F"
        //                     echo "Successfully killed process with PID ${pid}."
        //                 } catch (Exception e) {
        //                     echo "Warning: Could not kill process with PID ${pid}. It may have already exited. Error: ${e.getMessage()}"
        //                 }
        //                 sh 'rm django_server.pid'
        //             } else {
        //                 echo "PID file not found. Server may not have been started or already stopped."
        //             }
        //         }
        //     }
        // }
    }

    post {
        always {
            stage('Kill Django Server') {
                steps {
                    echo "💀 Killing Django server process..."
                    script {
                        if (fileExists('django_server.pid')) {
                            // Читаем PID из файла
                            def pid = readFile('django_server.pid').trim()
                            
                            // Завершаем процесс, используя taskkill
                            // /F - принудительно, /T - завершает дочерние процессы (включая cmd)
                            try {
                                bat "taskkill /PID ${pid} /F /T"
                                echo "Successfully killed process with PID ${pid}."
                            } catch (Exception e) {
                                echo "Warning: Process with PID ${pid} may have already exited. Error: ${e.getMessage()}"
                            }
                            
                            // Удаляем временный файл
                            bat 'del django_server.pid'
                        } else {
                            echo "PID file not found. Server was not started or was stopped earlier."
                        }
                    }
                }
            }
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