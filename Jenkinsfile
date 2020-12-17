pipeline {
    agent any
    stages {
        stage('Trigger') {
            steps {
                build job: 'msws-base', wait: false
            }
        }
    }
}