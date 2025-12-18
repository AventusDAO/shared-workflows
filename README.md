# Shared Workflows

Infrastructure related scripts/automations and reusable GitHub Actions workflows.

This repository hosts reusable GitHub Actions workflows that can be used across multiple repositories in the AventusDAO organization.

## Documentation

- **[CHANGELOG.md](./CHANGELOG.md)** - Complete list of available workflows, their features, and version history
- **[MIGRATION.md](./MIGRATION.md)** - Migration guide from previous versions to current (v5.20.0) with breaking changes and step-by-step instructions

## Quick Start

### Using a Reusable Workflow

```yaml
name: My Workflow

on:
  push:
    branches:
      - main

jobs:
  my-job:
    uses: AventusDAO/shared-workflows/.github/workflows/workflow-name.yaml@VERSION
    with:
      # Input parameters
    secrets:
      # Required secrets
```

### Example: Automatic Releases

```yaml
name: Automatic Release

on:
  push:
    branches:
      - main

jobs:
  github-release:
    uses: AventusDAO/shared-workflows/.github/workflows/automatic-releases.yaml@v5.20.0
    with:
      default_bump: minor
    secrets:
      envPat: ${{ secrets.GITHUB_TOKEN }}
```

See [MIGRATION.md](./MIGRATION.md) for more examples and detailed documentation.

## Available Workflows

1. **Automatic Releases** - Version bumping and GitHub release creation
2. **Check Yarn Application** - Build and validate Yarn/TypeScript applications
3. **Terraform Deploy** - Terraform validation, planning, and deployment
4. **Terraform Check** - Pre-commit checks for Terraform code
5. **Terraform Docs** - Automatic Terraform documentation generation
6. **Docker Build** - Build and push Docker images to AWS ECR

For complete details, see [CHANGELOG.md](./CHANGELOG.md).

