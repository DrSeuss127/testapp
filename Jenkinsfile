pipeline {
  environment {
            JACOCO_VERSION = '0.8.8'
            SONARQUBE_VERSION = '3.9.1.2184'
            PROJECT_NAME = 'testapp'
            QUALITY_GATE_SUCCESS = true
            PR_STATE = 'success'
            PR_DESCRIPTION = 'Build Successful!'
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
    stage('SonarQube Analysis') {
      steps {
        container('maven') {
          withSonarQubeEnv('sonarqube')
          sh "mvn clean org.jacoco:jacoco-maven-plugin:${env.JACOCO_VERSION}:prepare-agent test"
          sh "mvn org.jacoco:jacoco-maven-plugin:${env.JACOCO_VERSION}:report org.sonarsource.scanner.maven:sonar-maven-plugin:${env.SONARQUBE_VERSION}:sonar -Dsonar.projectKey=${env.PROJECT_NAME} -Dsonar.java.coveragePlugin=jacoco -Dsonar.dynamicAnalysis=reuseReports verify"
          sh """curl -X 'POST' \
              "https://defectdojo.aws.devops.com.ph/api/v2/reimport-scan"/ \
              -H 'accept:application/json' \
              -H 'Authorization:Token 10498fe57df09d7cf800601657ac931a366b31b2' \
              -H 'Content-Type:multipart/form-data' \
              -F 'test=102' \
              -F 'scan_type=SonarQube API Import' \
              -F 'api_scan_configuration=SonarQube Bug findings(testapp)'
              -F 'tags=test' 
              """
        }
      }
    }

    stage('Quality Gate') {
      steps {
        container('maven') {
          def qualityGate = waitForQualityGate()
          if (qualityGate.status != 'OK'){
            env.QUALITY_GATE_SUCCESS = false
            env.PR_STATE = 'failure'
            env.PR_DESCRIPTION = 'Build succeeded but failed on Quality Gate'
        }
      }
    }
  }
}
}