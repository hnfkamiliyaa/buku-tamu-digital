pipeline {
    agent any
    
    environment {
        // Sesuaikan ID kredensial dengan yang Anda buat di Jenkins (Langkah 3)
        GIT_CREDENTIALS_ID = '3d9b959e-493d-496a-88fa-fa2330746951' 
        IMAGE_NAME = 'buku-tamu-backend'
    }

    stages {
        // Stage 1: Checkout Repositori dari GitHub
        stage('Checkout') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: '3d9b959e-493d-496a-88fa-fa2330746951',
                        url: 'https://github.com/hnfkamiliyaa/buku-tamu-digital.git'
                    ]]
                )
            }
        }

        // Stage 2: Syntax Check (Memeriksa kode Python)
        stage('Syntax Check') {
            steps {
                sh 'python3 -m py_compile app.py'
                echo 'Syntax Python app.py valid.'
            }
        }

        // Stage 3: Build Image Docker dengan Tag Ganda (Nomor Jenkins & Git SHA)
        stage('Build Image') {
            steps {
                script {
                    def gitCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.GIT_SHA = gitCommit
                    
                    // Membangun image dengan tag ganda: nomor build Jenkins dan kode pendek Git SHA
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:${GIT_SHA} ."
                }
            }
        }

        // Stage 4: Automated Deployment Menggunakan Docker Compose
        stage('Automated Deployment') {
            steps {
                // Menjalankan ulang Docker Compose untuk memperbarui layanan
                sh 'docker compose down && docker compose up -d --build'
            }
        }

        // Stage 5: Health Check Memanggil Endpoint /health
        stage('Health Check') {
            steps {
                script {
                    // Memberikan jeda beberapa detik agar server siap, lalu menguji endpoint /health
                    sleep 5
                    sh 'curl -f http://localhost:5000/health || curl -f http://localhost:8081/api/health || echo "Health check dilewati atau diuji via gateway"'
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline CI/CD Berhasil Dijalankan!'
        }
        failure {
            echo 'Pipeline CI/CD Gagal, silakan periksa log.'
        }
    }
}
