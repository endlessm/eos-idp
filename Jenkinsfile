// The image tag. For a pull request, the tag will be named pr<number>.
// Otherwise the TAG parameter is used.
def tag = params.ghprbPullId ? 'pr' + params.ghprbPullId : params.TAG
assert tag != null

// Registry URL and credentials to use for pushing.
def registry = params.REGISTRY ?: 'https://index.docker.io/v1/'
def credentials = params.CREDENTIALS ?: 'dockerhub-endlessci'

node {
    def image

    stage('Build') {
        checkout scm
        image = docker.build("endlessm/eos-idp:${tag}")
    }

    stage('Test') {
        image.inside {
            sh './manage.py test --settings eosidp.settings.test'
        }
    }

    stage('Publish') {
        docker.withRegistry(registry, credentials) {
            image.push()
        }
    }
}
