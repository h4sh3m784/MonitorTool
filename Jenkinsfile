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

    stage('Upload files to S3'){
        sh("aws s3 cp src s3://${STATIC_S3_BUCKET_NAME} --recursive")
    }
}