node{

    stage('Clone repo'){
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }

    stage('Deploy serverless'){
        dir('serverless'){
            sh('sudo SLS_DEBUG=* sls deploy -v')
        }
    }
}