# Advanced Workflows

Complex scenarios and advanced usage patterns for CSS Kustomize.

## Multi-Environment Deployments

### Environment-Specific Configurations

```bash
# Development environment
poetry run dagger-pipeline generate-overlay without-pvc manifests/dev.yaml

# Staging environment  
poetry run dagger-pipeline generate-overlay with-pvc manifests/staging.yaml

# Production environment
poetry run dagger-pipeline generate-overlay with-pvc manifests/prod.yaml
```

### Automated Environment Promotion

```bash
#!/bin/bash
# promote-environment.sh

ENVIRONMENT=$1
VERSION=$2

case $ENVIRONMENT in
  "staging")
    OVERLAY="without-pvc"
    ;;
  "production")
    OVERLAY="with-pvc"
    ;;
  *)
    echo "Unknown environment: $ENVIRONMENT"
    exit 1
    ;;
esac

# Update version
poetry run dagger-pipeline update-overlay-version $OVERLAY $VERSION

# Validate and generate
poetry run dagger-pipeline validate-versions
poetry run dagger-pipeline generate-overlay $OVERLAY manifests/$ENVIRONMENT.yaml

# Deploy
kubectl apply -f manifests/$ENVIRONMENT.yaml
```

## Custom Overlay Development

### Creating New Overlays

```bash
# Create new overlay directory
mkdir -p overlays/custom-env

# Create kustomization.yaml
cat > overlays/custom-env/kustomization.yaml << EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: custom-namespace

resources:
  - ../../base

labels:
  - includeSelectors: false
    pairs:
      app.kubernetes.io/instance: css-custom
      app.kubernetes.io/version: "6.0.3"
      environment: custom

images:
  - name: solidproject/community-server
    newTag: "6.0.3"

patches:
  - target:
      kind: Deployment
      name: community-solid-server
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 3
EOF
```

### Advanced Patching

```yaml
# overlays/custom-env/resource-patches.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

patches:
  # Add resource limits
  - target:
      kind: Deployment
      name: community-solid-server
    patch: |-
      - op: add
        path: /spec/template/spec/containers/0/resources
        value:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
  
  # Add environment variables
  - target:
      kind: Deployment
      name: community-solid-server
    patch: |-
      - op: add
        path: /spec/template/spec/containers/0/env
        value:
          - name: CSS_CONFIG
            value: "/config/custom-config.json"
          - name: CSS_LOG_LEVEL
            value: "debug"
```

## Pipeline Customization

### Custom Validation Rules

```python
# custom_validators.py
import yaml
from pathlib import Path

def validate_custom_rules(overlay_path: str) -> bool:
    """Custom validation rules for overlays."""
    kustomization_path = Path(overlay_path) / "kustomization.yaml"
    
    with open(kustomization_path) as f:
        config = yaml.safe_load(f)
    
    # Ensure namespace is set
    if "namespace" not in config:
        print(f"ERROR: {overlay_path} missing namespace")
        return False
    
    # Ensure resource limits are set for production
    if "prod" in overlay_path:
        patches = config.get("patches", [])
        has_resource_limits = any(
            "resources" in str(patch) for patch in patches
        )
        if not has_resource_limits:
            print(f"ERROR: {overlay_path} missing resource limits")
            return False
    
    return True
```

### Extended Security Scanning

```bash
#!/bin/bash
# advanced-security-scan.sh

echo "🔍 Running advanced security scans..."

# Generate all manifests
poetry run dagger-pipeline generate manifests/

# Custom security checks
echo "Checking for privileged containers..."
if grep -r "privileged: true" manifests/; then
    echo "❌ Found privileged containers"
    exit 1
fi

echo "Checking for root users..."
if grep -r "runAsUser: 0" manifests/; then
    echo "❌ Found containers running as root"
    exit 1
fi

echo "Checking for host network access..."
if grep -r "hostNetwork: true" manifests/; then
    echo "❌ Found containers with host network access"
    exit 1
fi

echo "Checking for missing security contexts..."
for manifest in manifests/*.yaml; do
    if ! grep -q "securityContext" "$manifest"; then
        echo "⚠️  Missing security context in $manifest"
    fi
done

echo "✅ Advanced security scan completed"
```

## Parallel Processing Workflows

### Concurrent Overlay Processing

```python
# parallel_processing.py
import asyncio
import dagger
from pathlib import Path

async def process_overlays_parallel():
    """Process multiple overlays in parallel."""
    overlays = ["with-pvc", "without-pvc"]
    
    async with dagger.Connection() as client:
        tasks = []
        for overlay in overlays:
            task = generate_and_validate_overlay(client, overlay)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for overlay, result in zip(overlays, results):
            if isinstance(result, Exception):
                print(f"❌ {overlay}: {result}")
            else:
                print(f"✅ {overlay}: Success")

async def generate_and_validate_overlay(client, overlay_name):
    """Generate and validate a single overlay."""
    # Generate manifest
    manifest = await generate_overlay(client, overlay_name)
    
    # Validate manifest
    await validate_manifest(client, manifest)
    
    # Security scan
    await security_scan_manifest(client, manifest)
    
    return f"Processed {overlay_name}"
```

### Batch Operations

```bash
#!/bin/bash
# batch-operations.sh

OPERATIONS=("lint" "validate" "security-scan")
OVERLAYS=("with-pvc" "without-pvc")

# Run operations in parallel
for op in "${OPERATIONS[@]}"; do
    echo "🚀 Running $op..."
    poetry run dagger-pipeline $op --parallel &
done

# Wait for all operations to complete
wait

echo "✅ All batch operations completed"

# Generate all overlays in parallel
echo "📦 Generating manifests..."
poetry run dagger-pipeline generate --parallel manifests/

echo "🎉 Batch processing complete!"
```

## Integration with External Systems

### GitOps Integration

```yaml
# .github/workflows/gitops.yml
name: GitOps Deployment

on:
  push:
    branches: [main]
    paths: ['overlays/**', 'base/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
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
      
      - name: Run CI pipeline
        run: poetry run dagger-pipeline ci --parallel --verbose
      
      - name: Generate manifests
        run: poetry run dagger-pipeline generate manifests/
      
      - name: Deploy to staging
        if: github.ref == 'refs/heads/main'
        run: |
          kubectl apply -f manifests/with-pvc.yaml
          kubectl rollout status deployment/css-with-pvc
```

### Monitoring Integration

```python
# monitoring_integration.py
import requests
import json
from datetime import datetime

def send_metrics_to_prometheus(metrics):
    """Send custom metrics to Prometheus."""
    prometheus_gateway = "http://prometheus-pushgateway:9091"
    
    for metric_name, value in metrics.items():
        payload = f"{metric_name} {value}\n"
        
        response = requests.post(
            f"{prometheus_gateway}/metrics/job/css-kustomize",
            data=payload,
            headers={'Content-Type': 'text/plain'}
        )
        
        if response.status_code != 200:
            print(f"Failed to send metric {metric_name}: {response.text}")

def collect_pipeline_metrics():
    """Collect metrics from pipeline execution."""
    return {
        "css_kustomize_build_duration_seconds": 45.2,
        "css_kustomize_overlays_generated": 4,
        "css_kustomize_security_issues": 0,
        "css_kustomize_lint_errors": 0
    }

# Usage in pipeline
metrics = collect_pipeline_metrics()
send_metrics_to_prometheus(metrics)
```

## Advanced Testing Strategies

### Integration Testing

```bash
#!/bin/bash
# integration-test.sh

echo "🧪 Running integration tests..."

# Start test cluster
kind create cluster --name css-test

# Generate and apply manifests
poetry run dagger-pipeline generate manifests/
kubectl apply -f manifests/without-pvc.yaml

# Wait for deployment
kubectl wait --for=condition=available --timeout=300s deployment/css-local

# Test application endpoints
kubectl port-forward service/css-local 3000:3000 &
PF_PID=$!

sleep 5

# Test health endpoint
if curl -f http://localhost:3000/.well-known/solid; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Cleanup
kill $PF_PID
kind delete cluster --name css-test

echo "🎉 Integration tests completed"
```

### Performance Testing

```python
# performance_test.py
import time
import subprocess
import statistics

def measure_pipeline_performance():
    """Measure pipeline execution times."""
    operations = [
        "lint --yaml-only",
        "lint --python-only", 
        "validate",
        "security-scan"
    ]
    
    results = {}
    
    for op in operations:
        times = []
        for _ in range(3):  # Run 3 times
            start = time.time()
            subprocess.run(
                f"poetry run dagger-pipeline {op}",
                shell=True,
                check=True,
                capture_output=True
            )
            end = time.time()
            times.append(end - start)
        
        results[op] = {
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "min": min(times),
            "max": max(times)
        }
    
    return results

# Generate performance report
perf_results = measure_pipeline_performance()
for op, stats in perf_results.items():
    print(f"{op}: {stats['mean']:.2f}s (±{stats['max']-stats['min']:.2f}s)")
```

## Disaster Recovery

### Backup and Restore

```bash
#!/bin/bash
# backup-restore.sh

backup_configs() {
    echo "📦 Backing up configurations..."
    
    # Create backup directory
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup overlays
    cp -r overlays/ "$BACKUP_DIR/"
    cp -r base/ "$BACKUP_DIR/"
    
    # Backup generated manifests
    cp -r manifests/ "$BACKUP_DIR/"
    
    # Create metadata
    cat > "$BACKUP_DIR/metadata.json" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "git_commit": "$(git rev-parse HEAD)",
    "git_branch": "$(git branch --show-current)"
}
EOF
    
    echo "✅ Backup created: $BACKUP_DIR"
}

restore_configs() {
    BACKUP_DIR=$1
    
    if [[ ! -d "$BACKUP_DIR" ]]; then
        echo "❌ Backup directory not found: $BACKUP_DIR"
        exit 1
    fi
    
    echo "🔄 Restoring from backup: $BACKUP_DIR"
    
    # Restore configurations
    cp -r "$BACKUP_DIR/overlays/" .
    cp -r "$BACKUP_DIR/base/" .
    
    # Regenerate manifests
    poetry run dagger-pipeline generate manifests/
    
    echo "✅ Restore completed"
}

case $1 in
    "backup")
        backup_configs
        ;;
    "restore")
        restore_configs $2
        ;;
    *)
        echo "Usage: $0 {backup|restore <backup_dir>}"
        exit 1
        ;;
esac
```

## Next Steps

- Explore [CI/CD Integration](cicd-integration.md) patterns
- Review [Basic Usage](basic-usage.md) examples
- Check [Developer Guide](../developer-guide/architecture.md)
- Learn about [Dagger Pipeline](../developer-guide/dagger-pipeline.md) internals
