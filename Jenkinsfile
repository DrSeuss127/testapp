pipeline {
  environment {
            JACOCO_VERSION = '0.8.8'
            SONARQUBE_VERSION = '3.9.1.2184'
            PROJECT_NAME = 'testapp'
            QUALITY_GATE_SUCCESS = true
            PR_STATE = 'success'
            PR_DESCRIPTION = 'Build Successful!'

            // Defect Dojo Environment Variables
            HOST_NAME = "https://defectdojo.aws.devops.com.ph/api/v2/reimport-scan"
            TOKEN = "10498fe57df09d7cf800601657ac931a366b31b2"
  }
  agent{
    kubernetes {
      yaml '''
          apiVersion: v1
          kind: Pod
          metadata:
            labels:
              some-label: test

          spec:
            containers:

            - name: alpine
              image: alpine:latest
              volumeMounts:
              - mountPath: "/var/jenkins_home/"
                name: "jenkins"
                readOnly: false
              command:
              - cat
              tty: true
            
            - name: maven
              image: maven:3.8.6-jdk-11
              command:
              - cat
              tty: true

            volumes:
            - name: jenkins
              persistentVolumeClaim:
                claimName: jjb-pvc
          '''
    }
  }
  stages {
    stage('Install Python') {
      steps {
        container('alpine') {
            sh 'apk add --update python3'
            sh 'python3 -m ensurepip'
            sh 'pip3 install --upgrade pip setuptools'
            sh 'apk add --update python3-dev'
        }
            
      }
    }
    stage('Install Semgrep') {
      steps {
        container('alpine') {
            sh 'apk add --upgrade alpine-sdk'
            sh 'apk add gcc'
            sh 'python3 -m pip install semgrep'
        }
      }
    }
    stage('Semgrep-Scan') {
      steps {
        container('alpine') {
            sh 'semgrep ci'
            sh 'semgrep scan --config auto --json -o scan.json'
            sh """curl -X 'POST' \
              "https://defectdojo.aws.devops.com.ph/api/v2/reimport-scan"/ \
              -H 'accept:application/json' \
              -H 'Authorization:Token 10498fe57df09d7cf800601657ac931a366b31b2' \
              -H 'Content-Type:multipart/form-data' \
              -F 'test=167' \
              -F 'file=@scan.json;type=application/json' \
              -F 'scan_type=Semgrep JSON Report' \
              -F 'tags=test' 
              """
        }
      }
    }
    // Scan Config can be found at: https://defectdojo.aws.devops.com.ph/api/v2/product_api_scan_configurations/
    stage('SonarQube Scan') {
        steps {
            container('maven') {    
            withSonarQubeEnv('sonarqube') {
                
                // Bug Finding
                sh """curl -X 'POST' \
                    "${env.HOST_NAME}"/ \
                    -H 'accept:application/json' \
                    -H 'Authorization:Token ${env.TOKEN}' \
                    -H 'Content-Type:multipart/form-data' \
                    -F 'test=232' \
                    -F 'scan_type=SonarQube API Import' \
                    -F 'api_scan_configuration=18' \
                    -F 'tags=test' 
                    """


                // Smell Finding
                sh """curl -X 'POST' \
                    "${env.HOST_NAME}"/ \
                    -H 'accept:application/json' \
                    -H 'Authorization:Token ${env.TOKEN}' \
                    -H 'Content-Type:multipart/form-data' \
                    -F 'test=233' \
                    -F 'scan_type=SonarQube API Import' \
                    -F 'api_scan_configuration=19' \
                    -F 'tags=test' 
                    """

                // Vulnerabilities Finding
                sh """curl -X 'POST' \
                    "${env.HOST_NAME}"/ \
                    -H 'accept:application/json' \
                    -H 'Authorization:Token ${env.TOKEN}' \
                    -H 'Content-Type:multipart/form-data' \
                    -F 'test=234' \
                    -F 'scan_type=SonarQube API Import' \
                    -F 'api_scan_configuration=20' \
                    -F 'tags=test' 
                    """
                }
                
            }
        }
    }

    stage ('Evaluate Findings') {
        steps {
            container('alpine') {
                sh 'python3 evaluate_findings.py'
            }
        }
    }

    stage ('Quality Gate') {
        steps {
            container('maven') {
                withSonarQubeEnv('sonarqube') {
                    // Use JaCoCo (Java Code Coverage) to measure code coverage
                    // Use SonarScanner to analyze code coverage produced by JaCoCo
                    sh "mvn clean org.jacoco:jacoco-maven-plugin:${env.JACOCO_VERSION}:prepare-agent test"
                    sh "mvn org.jacoco:jacoco-maven-plugin:${env.JACOCO_VERSION}:report org.sonarsource.scanner.maven:sonar-maven-plugin:${env.SONARQUBE_VERSION}:sonar -Dsonar.projectKey=${env.PROJECT_NAME} -Dsonar.java.coveragePlugin=jacoco -Dsonar.dynamicAnalysis=reuseReports verify"
                }
            }

            script {
                //Throw an error to fail the build when SonarScanner does not pass the project
                def qualityGate = waitForQualityGate()
                if (qualityGate.status != "OK") {
                    env.QUALITY_GATE_SUCCESS = false
                    env.PR_STATE = 'failure'
                    env.PR_DESCRIPTION = 'Build Succeeded but failed on quality gate'
                }
            } 
        }
    }
  }
}