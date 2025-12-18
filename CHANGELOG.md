# Changelog

All notable changes to the shared workflows will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Available Workflows

### Reusable Workflows

#### 1. Automatic Releases (`automatic-releases.yaml`)
**Purpose**: Automatically bump version, create git tags, and generate GitHub releases.

**Current Version**: `v5.20.0` (Latest)

**Inputs**:
- `agent` (optional, default: `ubuntu-latest`): Agent where the workflow will run
- `default_bump` (optional, default: `none`): Default version bump type (major, minor, patch, none)

**Secrets**:
- `envPat` (required): GitHub token for authentication

**Features**:
- Automatic version bumping using semantic versioning
- Git tag creation with `v` prefix
- GitHub release creation with auto-generated release notes
- Skips version bumping on initial commits

---

#### 2. Check Yarn Application (`check-yarn-application.yml`)
**Purpose**: Check, build, and validate Yarn-based applications.

**Inputs**:
- `agent` (optional, default: `ubuntu-latest`): Agent where the workflow will run
- `checkout_repository` (optional): Repository to checkout (owner/repo format)
- `checkout_ref` (optional): Git ref to checkout (branch, tag, or commit SHA)
- `checkout_depth` (optional, default: `0`): Depth of checkout
- `node_version` (optional, default: `18.6`): Node.js version to use
- `cache` (optional, default: `yarn`): Package manager cache type
- `install_dependencies` (optional, default: `true`): Whether to install dependencies
- `build_packages` (optional, default: `true`): Whether to build packages
- `build_command` (optional): Custom build command
- `run_checks` (optional, default: `true`): Whether to run TypeScript checks
- `working_directory` (optional, default: `.`): Working directory for commands

**Features**:
- Node.js setup with version management
- Yarn dependency installation
- Package building
- TypeScript type checking

---

#### 3. Terraform Deploy (`terraform-workflow.yml`)
**Purpose**: Deploy and manage Terraform infrastructure with validation, planning, and optional auto-apply.

**Inputs**:
- `agent` (optional, default: `ubuntu-latest`): Agent where the workflow will run
- `checkout_repository` (optional): Repository to checkout (owner/repo format)
- `checkout_ref` (optional): Git ref to checkout (branch, tag, or commit SHA)
- `checkout_depth` (optional, default: `0`): Depth of checkout
- `phyton_version` (optional): Python version to download
- `auto_apply` (optional, default: `false`): Whether to automatically apply changes
- `target_branch` (optional, default: `main`): Target branch where changes should be applied
- `aws_region` (optional, default: `eu-west-1`): AWS region for deployment
- `setup_ssh` (optional, default: `false`): Whether to setup SSH for the workflow

**Secrets**:
- `AWS_ACCESS_KEY_ID` (required): AWS access key ID
- `AWS_SECRET_ACCESS_KEY` (required): AWS secret access key
- `GH_TOKEN` (required): GitHub token for API access
- `SSH_PRIVATE_KEY` (optional): SSH private key for authentication

**Features**:
- Terraform initialization and validation
- Terraform plan generation with PR comments
- Optional auto-apply on target branch
- AWS credential management
- SSH setup for private repositories
- Python environment setup

---

#### 4. Terraform Check (`check-workflow.yml`)
**Purpose**: Run pre-commit checks on Terraform code including formatting, linting, and validation.

**Inputs**:
- `agent` (optional, default: `ubuntu-latest`): Agent where the workflow will run
- `checkout_repository` (optional): Repository to checkout (owner/repo format)
- `checkout_ref` (optional): Git ref to checkout (branch, tag, or commit SHA)
- `checkout_depth` (optional, default: `0`): Depth of checkout

**Features**:
- Pre-commit hook installation
- TFLint installation and execution
- Terraform formatting checks
- Terraform validation
- Runs checks on all files

---

#### 5. Terraform Docs (`terraform-docs-workflow.yml`)
**Purpose**: Generate and update Terraform documentation in README files.

**Inputs**:
- `agent` (optional, default: `ubuntu-latest`): Agent where the workflow will run
- `checkout_repository` (optional): Repository to checkout (owner/repo format)
- `checkout_ref` (optional): Git ref to checkout (branch, tag, or commit SHA)
- `checkout_depth` (optional, default: `0`): Depth of checkout

**Features**:
- Automatic Terraform documentation generation
- Updates README.md with generated docs
- Pushes changes back to PR automatically
- Uses replace method for documentation sections

---

#### 6. Docker Build (`docker-build.yaml`)
**Purpose**: Build and push Docker images to AWS ECR (private or public).

**Inputs**:
- `ecr_registry_type` (optional, default: `private`): ECR registry type (private/public)
- `ecr_public_alias` (optional, default: `aventus`): Public ECR alias
- `agent` (optional, default: `arc-ubuntu-2404-x64`): Agent where the workflow will run
- `checkout_repository` (optional): Repository to checkout (owner/repo format)
- `checkout_ref` (optional): Git ref to checkout (branch, tag, or commit SHA)
- `checkout_depth` (optional, default: `0`): Depth of checkout
- `config_creds` (optional, default: `true`): Whether to configure AWS credentials
- `artifact_name` (optional): Name of artifact to download before build
- `aws_region` (required): AWS region for ECR
- `aws_account_id` (required): AWS account ID
- `git_context` (optional, default: `.`): Git context path
- `docker_file_path` (optional, default: `./Dockerfile`): Path to Dockerfile
- `ecr_repository_name` (required): ECR repository name
- `default_branch` (optional, default: `master`): Default branch name
- `create_pr_dtag` (optional, default: `false`): Create PR tag (pr-{number})
- `create_latest_dtag` (optional, default: `false`): Create latest tag
- `create_commit_hash_dtag` (optional, default: `false`): Create commit hash tag
- `create_git_ref_dtag` (optional, default: `false`): Create git ref tag
- `docker_args_list` (optional): Docker build arguments

**Secrets**:
- `aws_access_key` (optional): AWS access key
- `aws_secret_key` (optional): AWS secret key

**Features**:
- Support for both private and public ECR registries
- Multiple tagging strategies (PR, latest, commit hash, git ref)
- Artifact download support
- Docker Buildx setup
- AWS credential management (key-based or role-based)

---

## Version History

### v5.20.0 (Latest)
- Latest version - See release notes for details

### v5.19.0
- Updated terraform workflows with new checkout inputs
- Updated actions/checkout@v4 → v6
- Updated actions/setup-python@v4 → v6
- Used in `automatic-repo-release.yaml` example
