pipeline {
  agent any
  stages {
    stage('Semgrep-Scan') {
        environment { 
          // Add the rules that Semgrep uses by setting the SEMGREP_RULES environment variable. 
          SEMGREP_RULES = "p/default"
          // Scan changed files in PRs or MRs (diff-aware scanning):
          // SEMGREP_BASELINE_REF = "${GIT_BRANCH}"
          // Uncomment SEMGREP_TIMEOUT to set this job's timeout (in seconds):
          // Default timeout is 1800 seconds (30 minutes).
          // Set to 0 to disable the timeout.
          // SEMGREP_TIMEOUT = "300"
        } 
      steps {
        container('alpine'){
            sh 'apk update && apk upgrade --available'
            sh 'apk add --update python3'
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
}