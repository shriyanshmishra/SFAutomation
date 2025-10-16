pipeline {
    agent any

    environment {
        SF_ALIAS = "RealEstateDemoScratch"
        DEV_HUB_ALIAS = "DevHub"
        SF_USERNAME = credentials('sf-username')                // Dev Hub user's email
        CONNECTED_APP_CONSUMER_KEY = credentials('sf-client-id')// Connected App Consumer Key
        JWT_KEY_FILE = credentials('sf-jwt-key')                // server.key (private key file)
        PYTHON = "python3"
        VENV_DIR = "venv"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Authenticate with Salesforce Dev Hub') {
            steps {
                echo 'Authenticating with Salesforce using JWT...'
                sh """
                sf org login jwt \
                  --username "${SF_USERNAME}" \
                  --jwt-key-file "${JWT_KEY_FILE}" \
                  --client-id "${CONNECTED_APP_CONSUMER_KEY}" \
                  --set-default-dev-hub \
                  --alias "${DEV_HUB_ALIAS}"
                """
            }
        }

        stage('Delete old scratch org') {
            steps {
                script {
                    echo "Checking for existing scratch org..."
                    def exists = sh(script: "sf org list --all | grep ${SF_ALIAS} || true", returnStatus: true)
                    if (exists == 0) {
                        echo "Deleting existing scratch org..."
                        sh "sf org delete scratch --target-org ${SF_ALIAS} -p || true"
                    } else {
                        echo "No old org found, skipping..."
                    }
                }
            }
        }

        stage('Create scratch org') {
            steps {
                echo 'Creating scratch org...'
                sh "sf org create scratch -f config/project-scratch-def.json -a ${SF_ALIAS} --duration-days 7 --set-default"
            }
        }

        stage('Push Metadata') {
            steps {
                echo 'Deploying metadata to scratch org...'
                sh "sf project deploy start"
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh """
                ${PYTHON} -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                python -m pip install --upgrade pip
                pip install pandas
                """
            }
        }

        stage('Generate Data CSVs') {
            steps {
                echo 'Generating CSVs from Excel data...'
                sh """
                . ${VENV_DIR}/bin/activate
                python scripts/generate_csv.py
                """
            }
        }

        stage('Import Demo Data') {
            steps {
                echo 'Importing Accounts, Contacts, and Opportunities...'
                sh """
                . ${VENV_DIR}/bin/activate
                python scripts/import_data.py
                """
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed — check logs for details."
        }
        always {
            echo "🧹 Cleaning up scratch org..."
            // Uncomment to delete scratch org at end of pipeline runs
            // sh "sf org delete scratch --target-org ${SF_ALIAS} -p || true"
        }
    }
}