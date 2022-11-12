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
            sh 'apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python'
            sh 'python3 -m ensurepip'
            sh 'pip3 install --no-cache --upgrade pip setuptools'
        }
            
      }
    }
    stage('Semgrep-Scan') {
      steps {
        container('alpine') {
            sh 'apk add gcc && ln -sf gcc /usr/bin/gcc'
            sh 'python3 -m pip install semgrep'
            sh 'semgrep ci'
            sh 'semgrep scan --config auto --json -o semgrep.json'
            sh '''curl -X \'POST\' \\
                \'http://devkinetics.az.devops.com.ph/api/v2/reimport-scan/\' \\
                -H \'accept: application/json\' \\
                -H \'Authorization: Token $defectdojo_token\' \\
                -H \'Content-Type: multipart/form-data\' \\
                -F \'test=102\' \\
                -F \'file=@semgrep.json;type=application/json\' \\
                -F \'scan_type=Semgrep JSON Report\' \\
                -F \'tags=test\' \\'''
        }
      }
    }
  }
}