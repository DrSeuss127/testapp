pipeline {
  agent any
    environment {
      // The following variables are required for a Semgrep App-connected scan:
      SEMGREP_APP_TOKEN = credentials('SEMGREP_APP_TOKEN')
      SEMGREP_BRANCH = "${GIT_BRANCH}"

      // Uncomment the following line to scan changed 
      // files in PRs or MRs (diff-aware scanning): 
      // SEMGREP_BASELINE_REF = "main"

      // Optional:
      // Uncomment SEMGREP_TIMEOUT to set this job's timeout (in seconds).
      // Default timeout is 1800 seconds (30 minutes).
      // Set to 0 to disable the timeout.
      // SEMGREP_TIMEOUT = "300"

      // Troubleshooting:

      // Uncomment the following lines if Semgrep App > Findings Page does not create links
      // to the code that generated a finding.
      // (For Semgrep versions before 0.98.0)
      // SEMGREP_JOB_URL = "${BUILD_URL}"
      // SEMGREP_COMMIT = "${GIT_COMMIT}"
      // SEMGREP_PR_ID = "${env.CHANGE_ID}"
      
      // Uncomment the following lines if Semgrep App > Findings Page does not create links
      // to the code that generated a finding.
      // (Any Semgrep version.)
      // SEMGREP_REPO_NAME = env.GIT_URL.replaceFirst(/^https:\/\/github.com\/(.*).git$/, '$1')
      // SEMGREP_REPO_URL = env.GIT_URL.replaceFirst(/^(.*).git$/,'$1')

    }
    stages {
      stage('Semgrep-Scan') {
        steps {
          sh 'docker run --rm -v "${PWD}:/src" returntocorp/semgrep semgrep --config=auto'
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