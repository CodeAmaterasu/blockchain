pipeline {

    agent any

    stages {

        stage('Deploy') {
            environment {
                REMOTE_DIR = "/app/apps/blockchain"
                SOURCE_FILES = "**/*.py, Dockerfile, docker-compose.yml, .dockerignore, requirements.txt"
            }
            steps {
                echo "Deploying Blockchain"
                sshPublisher(
                    continueOnError: false,
                    failOnError: true,
                    publishers: [
                        sshPublisherDesc (
                            configName: "administrator@danilojakob.ch",
                            verbose: true,
                            transfers: [
                                sshTransfer (
                                    execCommand: "if [ -d ${REMOTE_DIR} ]; then " +
                                                    "cd ${REMOTE_DIR} && " +
                                                    "rm -rf *" +
                                                    "; fi \n"
                                ),
                                sshTransfer (
                                    sourceFiles: env.SOURCE_FILES,
                                    remoteDirectory: env.REMOTE_DIR,
                                    execCommand: "sudo docker-compose -f /app/apps/blockchain/docker-compose.yml up -d --build"
                                )
                            ]
                        )
                    ]
                )
            }
        }
    }

}