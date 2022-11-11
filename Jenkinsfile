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
            sh 'apt-get update'
            sh 'apt-get install python3'
      }
    }
    stage('Semgrep-Scan') {
      steps {
            sh 'pip3 install semgrep'
            sh 'semgrep ci'
            sh 'semgrep scan --config auto --json -o semgrep.json'
            sh '''curl -X \'POST\' \\
                \'http://devkinetics.az.devops.com.ph/api/v2/reimport-scan/\' \\
                -H \'accept: application/json\' \\
                -H \'Authorization: Token $defectdojo_token\' \\
                -H \'Content-Type: multipart/form-data\' \\
                -F \'test=69\' \\
                -F \'file=@semgrep.json;type=application/json\' \\
                -F \'scan_type=Semgrep JSON Report\' \\
                -F \'tags=test\' \\'''
      }
    }
  }
}