# CI/CD Integration

Integration patterns and examples for CSS Kustomize in various CI/CD platforms.

## GitHub Actions

### Basic CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint-and-validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: latest
          virtualenvs-create: true
          virtualenvs-in-project: true

      - name: Load cached venv
        id: cached-poetry-dependencies
        uses: actions/cache@v3
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}

      - name: Install dependencies
        if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
        run: poetry install --no-interaction --no-root

      - name: Install project
        run: poetry install --no-interaction

      - name: Run CI pipeline
        run: poetry run dagger-pipeline ci --parallel --verbose

      - name: Upload manifests
        uses: actions/upload-artifact@v3
        with:
          name: kubernetes-manifests
          path: manifests/
```

### Advanced CI/CD with Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  ci:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        uses: snok/install-poetry@v1

      - name: Install dependencies
        run: poetry install

      - name: Extract version
        id: version
        run: |
          if [[ $GITHUB_REF == refs/tags/* ]]; then
            VERSION=${GITHUB_REF#refs/tags/v}
          else
            VERSION="main-$(git rev-parse --short HEAD)"
          fi
          echo "version=$VERSION" >> $GITHUB_OUTPUT

      - name: Update version in manifests
        run: poetry run dagger-pipeline version update ${{ steps.version.outputs.version }}

      - name: Run CI pipeline
        run: poetry run dagger-pipeline ci --parallel --verbose

      - name: Generate manifests
        run: poetry run dagger-pipeline generate manifests/

      - name: Upload manifests
        uses: actions/upload-artifact@v3
        with:
          name: manifests-${{ steps.version.outputs.version }}
          path: manifests/

  deploy-staging:
    needs: ci
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - name: Download manifests
        uses: actions/download-artifact@v3
        with:
          name: manifests-${{ needs.ci.outputs.version }}
          path: manifests/

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'latest'

      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig

      - name: Deploy to staging
        run: |
          kubectl apply -f manifests/with-pvc.yaml
          kubectl rollout status deployment/css-with-pvc --timeout=300s

  deploy-production:
    needs: [ci, deploy-staging]
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production
    steps:
      - name: Download manifests
        uses: actions/download-artifact@v3
        with:
          name: manifests-${{ needs.ci.outputs.version }}
          path: manifests/

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3

      - name: Deploy to production
        run: |
          kubectl apply -f manifests/with-pvc.yaml
          kubectl rollout status deployment/css-with-pvc --timeout=600s
```

## GitLab CI

### Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - validate
  - build
  - deploy

variables:
  PYTHON_VERSION: "3.11"

before_script:
  - apt-get update -qq && apt-get install -y -qq git curl
  - curl -sSL https://install.python-poetry.org | python3 -
  - export PATH="$HOME/.local/bin:$PATH"
  - poetry --version

lint:
  stage: lint
  image: python:${PYTHON_VERSION}
  script:
    - poetry install
    - poetry run dagger-pipeline lint --parallel
  artifacts:
    reports:
      junit: reports/lint-results.xml
    when: always

validate:
  stage: validate
  image: python:${PYTHON_VERSION}
  script:
    - poetry install
    - poetry run dagger-pipeline validate
    - poetry run dagger-pipeline security-scan
  dependencies:
    - lint

build-manifests:
  stage: build
  image: python:${PYTHON_VERSION}
  script:
    - poetry install
    - poetry run dagger-pipeline generate manifests/
  artifacts:
    paths:
      - manifests/
    expire_in: 1 week
  dependencies:
    - validate

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl apply -f manifests/with-pvc.yaml
    - kubectl rollout status deployment/css-with-pvc
  environment:
    name: staging
    url: https://css-staging.example.com
  only:
    - main
  dependencies:
    - build-manifests

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl apply -f manifests/with-pvc.yaml
    - kubectl rollout status deployment/css-with-pvc
  environment:
    name: production
    url: https://css.example.com
  when: manual
  only:
    - tags
  dependencies:
    - build-manifests
```

### Advanced GitLab Pipeline

```yaml
# .gitlab-ci.yml (Advanced)
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

stages:
  - lint
  - test
  - security
  - build
  - deploy
  - monitor

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

.poetry_template: &poetry_template
  image: python:3.11
  before_script:
    - pip install poetry
    - poetry install
  cache:
    paths:
      - .venv/

lint-yaml:
  <<: *poetry_template
  stage: lint
  script:
    - poetry run dagger-pipeline lint --yaml-only
  artifacts:
    reports:
      junit: reports/yaml-lint.xml

lint-python:
  <<: *poetry_template
  stage: lint
  script:
    - poetry run dagger-pipeline lint --python-only
  artifacts:
    reports:
      junit: reports/python-lint.xml

validate-kustomize:
  <<: *poetry_template
  stage: test
  script:
    - poetry run dagger-pipeline validate
  dependencies:
    - lint-yaml

security-scan-configs:
  <<: *poetry_template
  stage: security
  script:
    - poetry run dagger-pipeline security-scan
  artifacts:
    reports:
      sast: reports/security-scan.json
  dependencies:
    - validate-kustomize

build-all-manifests:
  <<: *poetry_template
  stage: build
  script:
    - poetry run dagger-pipeline generate --parallel manifests/
    - poetry run dagger-pipeline security-scan-generated manifests/
  artifacts:
    paths:
      - manifests/
    reports:
      sast: reports/manifest-security.json
  dependencies:
    - security-scan-configs

.deploy_template: &deploy_template
  image: bitnami/kubectl:latest
  before_script:
    - echo "$KUBECONFIG_CONTENT" | base64 -d > kubeconfig
    - export KUBECONFIG=kubeconfig

deploy-review:
  <<: *deploy_template
  stage: deploy
  script:
    - kubectl create namespace css-review-$CI_MERGE_REQUEST_IID || true
    - kubectl apply -f manifests/without-pvc.yaml -n css-review-$CI_MERGE_REQUEST_IID
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    url: https://css-review-$CI_MERGE_REQUEST_IID.example.com
    on_stop: stop-review
  only:
    - merge_requests
  dependencies:
    - build-all-manifests

stop-review:
  <<: *deploy_template
  stage: deploy
  script:
    - kubectl delete namespace css-review-$CI_MERGE_REQUEST_IID
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    action: stop
  when: manual
  only:
    - merge_requests

deploy-staging:
  <<: *deploy_template
  stage: deploy
  script:
    - kubectl apply -f manifests/with-pvc.yaml
    - kubectl rollout status deployment/css-with-pvc --timeout=300s
  environment:
    name: staging
    url: https://css-staging.example.com
  only:
    - main
  dependencies:
    - build-all-manifests

deploy-production:
  <<: *deploy_template
  stage: deploy
  script:
    - kubectl apply -f manifests/with-pvc.yaml
    - kubectl rollout status deployment/css-with-pvc --timeout=600s
  environment:
    name: production
    url: https://css.example.com
  when: manual
  only:
    - tags
  dependencies:
    - build-all-manifests

monitor-deployment:
  stage: monitor
  image: curlimages/curl:latest
  script:
    - |
      for i in {1..30}; do
        if curl -f https://css.example.com/.well-known/solid; then
          echo "✅ Health check passed"
          exit 0
        fi
        echo "⏳ Waiting for service to be ready..."
        sleep 10
      done
      echo "❌ Health check failed"
      exit 1
  only:
    - tags
  dependencies:
    - deploy-production
```

## Jenkins

### Declarative Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m pip install poetry
                    poetry install
                '''
            }
        }
        
        stage('Lint') {
            parallel {
                stage('YAML Lint') {
                    steps {
                        sh 'poetry run dagger-pipeline lint --yaml-only'
                    }
                }
                stage('Python Lint') {
                    steps {
                        sh 'poetry run dagger-pipeline lint --python-only'
                    }
                }
            }
        }
        
        stage('Validate') {
            steps {
                sh 'poetry run dagger-pipeline validate'
            }
        }
        
        stage('Security Scan') {
            steps {
                sh 'poetry run dagger-pipeline security-scan'
            }
        }
        
        stage('Build Manifests') {
            steps {
                sh 'poetry run dagger-pipeline generate --parallel manifests/'
                archiveArtifacts artifacts: 'manifests/**/*.yaml', fingerprint: true
            }
        }
        
        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    tag pattern: 'v\\d+\\.\\d+\\.\\d+', comparator: 'REGEXP'
                }
            }
            steps {
                script {
                    if (env.BRANCH_NAME == 'main') {
                        sh '''
                            kubectl apply -f manifests/with-pvc.yaml
                            kubectl rollout status deployment/css-with-pvc
                        '''
                    } else if (env.TAG_NAME) {
                        input message: 'Deploy to production?', ok: 'Deploy'
                        sh '''
                            kubectl apply -f manifests/with-pvc.yaml
                            kubectl rollout status deployment/css-with-pvc --timeout=600s
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: '*.html',
                reportName: 'Pipeline Report'
            ])
        }
        failure {
            emailext (
                subject: "Pipeline Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Pipeline failed. Check console output at ${env.BUILD_URL}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

## Azure DevOps

### Azure Pipelines

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  tags:
    include:
      - v*

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.11'
  poetryVersion: '1.6.1'

stages:
- stage: CI
  displayName: 'CI Stage'
  jobs:
  - job: LintAndValidate
    displayName: 'Lint and Validate'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'
      displayName: 'Use Python $(pythonVersion)'

    - script: |
        python -m pip install --upgrade pip
        pip install poetry==$(poetryVersion)
        poetry install
      displayName: 'Install dependencies'

    - script: |
        poetry run dagger-pipeline lint --parallel
      displayName: 'Run linting'

    - script: |
        poetry run dagger-pipeline validate
      displayName: 'Validate Kustomize'

    - script: |
        poetry run dagger-pipeline security-scan
      displayName: 'Security scan'

    - script: |
        poetry run dagger-pipeline generate --parallel manifests/
      displayName: 'Generate manifests'

    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: 'manifests'
        artifactName: 'kubernetes-manifests'
      displayName: 'Publish manifests'

- stage: Deploy
  displayName: 'Deploy Stage'
  dependsOn: CI
  condition: and(succeeded(), or(eq(variables['Build.SourceBranch'], 'refs/heads/main'), startsWith(variables['Build.SourceBranch'], 'refs/tags/v')))
  jobs:
  - deployment: DeployToStaging
    displayName: 'Deploy to Staging'
    condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
    environment: 'staging'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: DownloadBuildArtifacts@0
            inputs:
              artifactName: 'kubernetes-manifests'
              downloadPath: '$(System.ArtifactsDirectory)'

          - task: Kubernetes@1
            inputs:
              connectionType: 'Kubernetes Service Connection'
              kubernetesServiceEndpoint: 'staging-k8s'
              command: 'apply'
              arguments: '-f $(System.ArtifactsDirectory)/kubernetes-manifests/with-pvc.yaml'

  - deployment: DeployToProduction
    displayName: 'Deploy to Production'
    condition: startsWith(variables['Build.SourceBranch'], 'refs/tags/v')
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: DownloadBuildArtifacts@0
            inputs:
              artifactName: 'kubernetes-manifests'
              downloadPath: '$(System.ArtifactsDirectory)'

          - task: Kubernetes@1
            inputs:
              connectionType: 'Kubernetes Service Connection'
              kubernetesServiceEndpoint: 'production-k8s'
              command: 'apply'
              arguments: '-f $(System.ArtifactsDirectory)/kubernetes-manifests/with-pvc.yaml'
```

## CircleCI

### Configuration

```yaml
# .circleci/config.yml
version: 2.1

orbs:
  python: circleci/python@2.1.1
  kubernetes: circleci/kubernetes@1.3.1

executors:
  python-executor:
    docker:
      - image: cimg/python:3.11
    working_directory: ~/project

jobs:
  lint-and-validate:
    executor: python-executor
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: poetry
      - run:
          name: Run linting
          command: poetry run dagger-pipeline lint --parallel
      - run:
          name: Validate Kustomize
          command: poetry run dagger-pipeline validate
      - run:
          name: Security scan
          command: poetry run dagger-pipeline security-scan

  build-manifests:
    executor: python-executor
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: poetry
      - run:
          name: Generate manifests
          command: poetry run dagger-pipeline generate --parallel manifests/
      - persist_to_workspace:
          root: .
          paths:
            - manifests

  deploy-staging:
    executor: kubernetes/default
    steps:
      - attach_workspace:
          at: .
      - kubernetes/install-kubectl
      - run:
          name: Deploy to staging
          command: |
            kubectl apply -f manifests/with-pvc.yaml
            kubectl rollout status deployment/css-with-pvc

  deploy-production:
    executor: kubernetes/default
    steps:
      - attach_workspace:
          at: .
      - kubernetes/install-kubectl
      - run:
          name: Deploy to production
          command: |
            kubectl apply -f manifests/with-pvc.yaml
            kubectl rollout status deployment/css-with-pvc --timeout=600s

workflows:
  version: 2
  ci-cd:
    jobs:
      - lint-and-validate
      - build-manifests:
          requires:
            - lint-and-validate
      - deploy-staging:
          requires:
            - build-manifests
          filters:
            branches:
              only: main
      - deploy-production:
          requires:
            - build-manifests
          filters:
            tags:
              only: /^v.*/
            branches:
              ignore: /.*/
```

## Best Practices

### Security Considerations

```yaml
# Security best practices for CI/CD
security_practices:
  secrets_management:
    - Use CI/CD platform secret management
    - Rotate secrets regularly
    - Limit secret access scope
    
  container_security:
    - Scan container images
    - Use minimal base images
    - Run as non-root user
    
  kubernetes_security:
    - Use RBAC for deployments
    - Scan manifests for security issues
    - Implement network policies
```

### Performance Optimization

```bash
# Caching strategies
cache_strategies:
  dependencies:
    - Cache Poetry virtual environments
    - Cache Docker layers
    - Cache Dagger build cache
    
  parallel_execution:
    - Run linting in parallel
    - Generate manifests concurrently
    - Use matrix builds for multiple environments
```

### Monitoring and Alerting

```yaml
# Monitoring integration
monitoring:
  health_checks:
    - Application readiness probes
    - Deployment status monitoring
    - Service availability checks
    
  alerting:
    - Pipeline failure notifications
    - Deployment status alerts
    - Security scan alerts
```

## Next Steps

- Review [Basic Usage](basic-usage.md) examples
- Explore [Advanced Workflows](advanced-workflows.md)
- Check [Developer Guide](../developer-guide/contributing.md)
- Learn about [Dagger Pipeline](../developer-guide/dagger-pipeline.md)
