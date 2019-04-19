node{

    def app

    stage('Clone repo'){
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }

    stage('Build Image'){
        app = docker.build("device-web-server")
    }

    stage('build device test'){
        GET_TOKEN = sh(
            script: "sudo aws ecr get-login --no-include-email --region eu-west-1 --debug",
            returnStdout: true
            ).trim()

        LOGIN = sh(
            script: "sudo ${GET_TOKEN}",
            retrunStdout: true
            )

            sh("sudo docker tag device-web-server 740976047420.dkr.ecr.eu-west-1.amazonaws.com/device-web-server:latest")
            sh("sudo docker push 740976047420.dkr.ecr.eu-west-1.amazonaws.com/device-web-server:latest")
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