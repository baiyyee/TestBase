pipeline {
    agent any

    environment {
        JobName = "DEMO"
    }

    stages {
        stage("run tests"){
            steps {
                sh "pytest"
            }
        }
    }

    post {
        always {
            junit "outputs/result.xml"
            emailext body: '${FILE,path="test_templates.html"}',
                     subject: "job ${env.JobName}, result: ${currentBuild.currentResult}",
                     to: "hhbstar@hotmail.com"
        }
    }
}