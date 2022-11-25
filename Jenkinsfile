pipeline {
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
  }
}