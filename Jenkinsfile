pipeline {
    agent any

    environment {
        // Убедитесь, что эта переменная будет содержать корректный email для уведомлений
        EMAIL_RECIPIENT = 'vlad.butakov.2004@mail.ru'
        VUE_DIR = 'client'
        DJANGO_DIR = '.'
    }

    stages {
        stage('Debug Branch Info') {
            steps {
                script {
                    echo "--- Сборка инициирована ---"
                    echo "GIT_BRANCH: '${env.GIT_BRANCH}'"
                    // Если это Merge Request, будут доступны следующие переменные:
                    if (env.CHANGE_ID) {
                        echo "Это Merge Request: ${env.CHANGE_ID}"
                        echo "Целевая ветка (Target Branch): ${env.CHANGE_TARGET}"
                        echo "Исходная ветка (Source Branch): ${env.CHANGE_BRANCH}"
                    } else {
                        echo "Это прямой пуш в ветку."
                    }
                    echo "----------------------------"
                }
            }
        }

        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                // SCM Checkout автоматически получит код MR/PR, если настроен Branch Source Plugin
                checkout scm
            }
        }

        stage('Install Python Dependencies') {
            // Запускаем установку зависимостей, если это dev, main или MR/PR
            when {
                anyOf {
                    branch 'dev'
                    branch 'main'
                    changeRequest() // Включает все Merge Requests (например, из fix/* в dev)
                }
            }
            steps {
                echo 'Installing Python dependencies (Django)...'
                // Используем powershell для более надежного выполнения в Windows
                powershell "pip install -r ${DJANGO_DIR}/requirements.txt"
            }
        }

        stage('Install Node.js Dependencies (Vue)') {
            // Запускаем установку зависимостей, если это dev, main или MR/PR
            when {
                anyOf {
                    branch 'dev'
                    branch 'main'
                    changeRequest() // Включает все Merge Requests (например, из fix/* в dev)
                }
            }
            steps {
                echo 'Installing Node.js dependencies (Vue frontend)...'
                powershell "cd ${VUE_DIR} ; npm install"
            }
        }

        stage('Build Vue.js Frontend') {
            // Запускаем сборку, если это dev, main или MR/PR
            when {
                anyOf {
                    branch 'dev'
                    branch 'main'
                    changeRequest() // Включает все Merge Requests (например, из fix/* в dev)
                }
            }
            steps {
                echo 'Building Vue.js application...'
                // Комманды для Windows/bat лучше заменить на powershell для большей универсальности
                powershell """
                    cd ${VUE_DIR}
                    npm run build
                    # Копирование собранных файлов
                    $targetDir = "${DJANGO_DIR}\\static\\frontend"
                    if (-not (Test-Path $targetDir)) {
                        mkdir $targetDir
                    }
                    Copy-Item -Path "${VUE_DIR}\\dist\\*" -Destination $targetDir -Recurse -Force
                """
                echo 'Vue.js built and copied to Django static/frontend folder.'
            }
        }

        stage('Run Django Tests') {
            // Запускаем тесты, если это dev, main или MR/PR
            when {
                anyOf {
                    branch 'dev'
                    branch 'main'
                    changeRequest() // Включает все Merge Requests (например, из fix/* в dev)
                }
            }
            steps {
                echo 'Running Django tests...'
                powershell "python ${DJANGO_DIR}/manage.py test --verbosity=2"
            }
            post {
                failure {
                    // Уведомление об ошибке после тестов
                    emailext(
                        subject: "TEST FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER} (${env.GIT_BRANCH})",
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
            // Деплой только при прямом пуше в main (после успешного Merge Request)
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to production...'
                // Переиспользуем команды сборки, чтобы обеспечить наличие свежего билда
                powershell """
                    cd ${VUE_DIR}
                    npm run build

                    $targetDir = "${DJANGO_DIR}\\static\\frontend"
                    if (-not (Test-Path $targetDir)) {
                        mkdir $targetDir
                    }
                    Copy-Item -Path "${VUE_DIR}\\dist\\*" -Destination $targetDir -Recurse -Force

                    "Deployment successful on branch main" | Out-File deployment.log
                    "Git commit: ${env.GIT_COMMIT}" | Out-File deployment.log -Append
                """

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
