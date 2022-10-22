pipeline {
  agent any
    stages {
      stage('Semgrep-Scan') {
        steps {
          sh 'apt install semgrep'
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