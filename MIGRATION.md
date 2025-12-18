# Migration Guide

This guide helps you migrate from previous versions of the shared workflows to the current version (v5.20.0).

## Table of Contents

1. [Migrating to v5.20.0](#migrating-to-v5200)
2. [Migrating to v5.19.0](#migrating-to-v5190)
3. [Migrating to v5.18.0](#migrating-to-v5180)
4. [Migrating to v5.15.0](#migrating-to-v5150)
5. [Breaking Changes Summary](#breaking-changes-summary)
6. [Step-by-Step Migration](#step-by-step-migration)

---

## Migrating to v5.20.0

**Release**: v5.20.0  
**Status**: Latest version

### Changes

#### Variable Name Change: `runner` → `agent`

**Breaking Change**: The input variable name has been standardized from `runner` to `agent` across all workflows for consistency.

**Affected Workflows**:
- `docker-build.yaml`
- `check-yarn-application.yml` (if using older versions)

**Migration Steps**:

1. **Update Docker Build Workflow**:
   ```yaml
   # Before (v5.17.0 and earlier)
   jobs:
     docker-build:
       uses: AventusDAO/shared-workflows/.github/workflows/docker-build.yaml@v5.17.0
       with:
         runner: "ubuntu-latest"  # ❌ Old variable name
         # ... other inputs
   
   # After (v5.20.0)
   jobs:
     docker-build:
       uses: AventusDAO/shared-workflows/.github/workflows/docker-build.yaml@v5.20.0
       with:
         agent: "ubuntu-latest"  # ✅ New variable name
         # ... other inputs
   ```

2. **Update Check Yarn Application Workflow** (if using v5.11.0 or earlier):
   ```yaml
   # Before
   jobs:
     check-app:
       uses: AventusDAO/shared-workflows/.github/workflows/check-yarn-application.yml@v5.11.0
       with:
         runner: "ubuntu-latest"  # ❌ Old variable name
   
   # After
   jobs:
     check-app:
       uses: AventusDAO/shared-workflows/.github/workflows/check-yarn-application.yml@v5.20.0
       with:
         agent: "ubuntu-latest"  # ✅ New variable name
   ```

**Note**: Other workflows (terraform-workflow.yml, check-workflow.yml, terraform-docs-workflow.yml, automatic-releases.yaml) already used `agent` from their initial creation, so no changes are needed for those.

---

## Migrating to v5.19.0

**Release**: v5.19.0  
**Date**: December 17, 2025  
**PR**: #33 - DEVOPS-1229 updated terraform workflows

### Changes

#### Terraform Workflow (`terraform-workflow.yml`)

**New Inputs Added**:
- `checkout_repository` (optional, default: `""`): Repository to checkout in owner/repo format
- `checkout_ref` (optional, default: `""`): Git ref to checkout (branch, tag, or commit SHA)
- `checkout_depth` (optional, default: `0`): Depth of checkout

**Action Updates**:
- `actions/checkout@v4` → `actions/checkout@v6`
- `actions/setup-python@v4` → `actions/setup-python@v6`

**Migration Steps**:

1. **Update your workflow version**:
   ```yaml
   # Before
   uses: AventusDAO/shared-workflows/.github/workflows/terraform-workflow.yml@v5.18.0
   
   # After
   uses: AventusDAO/shared-workflows/.github/workflows/terraform-workflow.yml@v5.19.0
   ```

2. **No action required** - The new inputs are optional and have defaults, so existing workflows will continue to work without changes.

3. **Optional: Use new checkout features**:
   ```yaml
   jobs:
     terraform:
       uses: AventusDAO/shared-workflows/.github/workflows/terraform-workflow.yml@v5.19.0
       with:
         checkout_repository: "owner/repo-name"  # Optional: checkout different repo
         checkout_ref: "branch-name"            # Optional: checkout specific branch/ref
         checkout_depth: 1                       # Optional: shallow clone
         # ... other inputs
   ```

#### Terraform Check Workflow (`check-workflow.yml`)

**New Inputs Added**:
- `checkout_repository` (optional, default: `""`): Repository to checkout
- `checkout_ref` (optional, default: `""`): Git ref to checkout

**Action Updates**:
- `actions/checkout@v4` → `actions/checkout@v6`

**Migration Steps**:

1. **Update your workflow version**:
   ```yaml
   # Before
   uses: AventusDAO/shared-workflows/.github/workflows/check-workflow.yml@v5.18.0
   
   # After
   uses: AventusDAO/shared-workflows/.github/workflows/check-workflow.yml@v5.19.0
   ```

2. **No breaking changes** - Existing workflows continue to work.

#### Terraform Docs Workflow (`terraform-docs-workflow.yml`)

**New Inputs Added**:
- `checkout_repository` (optional, default: `""`): Repository to checkout
- `checkout_ref` (optional, default: `""`): Git ref to checkout

**Action Updates**:
- `actions/checkout@v4` → `actions/checkout@v6`

**Breaking Change**:
- Removed hardcoded `ref: ${{ github.event.pull_request.head.ref }}`
- Now uses `ref: ${{ inputs.checkout_ref }}` which defaults to empty string (uses default branch)

**Migration Steps**:

1. **Update your workflow version**:
   ```yaml
   # Before
   uses: AventusDAO/shared-workflows/.github/workflows/terraform-docs-workflow.yml@v5.18.0
   
   # After
   uses: AventusDAO/shared-workflows/.github/workflows/terraform-docs-workflow.yml@v5.19.0
   ```

2. **If you need PR-specific checkout**, explicitly set `checkout_ref`:
   ```yaml
   jobs:
     terraform-docs:
       uses: AventusDAO/shared-workflows/.github/workflows/terraform-docs-workflow.yml@v5.19.0
       with:
         checkout_ref: ${{ github.event.pull_request.head.ref }}  # Add this for PRs
   ```

---

## Migrating to v5.18.0

**Release**: v5.18.0  
**Date**: December 17, 2025  
**PR**: #32 - DEVOPS-1236 - update org

### Changes

**Organization Change**:
- Repository organization changed from `Aventus-Network-Services` to `AventusDAO`

**Migration Steps**:

1. **Update all workflow references**:
   ```yaml
   # Before
   uses: Aventus-Network-Services/shared-workflows/.github/workflows/workflow-name.yaml@VERSION
   
   # After
   uses: AventusDAO/shared-workflows/.github/workflows/workflow-name.yaml@VERSION
   ```

2. **Update version tags** - Ensure you're using v5.18.0 or later:
   ```yaml
   # Example
   uses: AventusDAO/shared-workflows/.github/workflows/automatic-releases.yaml@v5.18.0
   ```

3. **Verify access** - Ensure your repositories have access to the `AventusDAO` organization.

**Affected Workflows**:
- All reusable workflows that reference the old organization name

---

## Migrating to v5.15.0

**Release**: v5.15.0  
**Date**: December 4, 2025  
**PR**: #29 - DEVOPS-1225 - update docker build to work with public repos and use arc runner by default

### Changes

#### Docker Build Workflow (`docker-build.yaml`)

**New Features**:
- Support for public ECR registries
- Default agent changed to `arc-ubuntu-2404-x64` (from `ubuntu-latest`)

**New Inputs**:
- `ecr_registry_type` (optional, default: `private`): Can be `private` or `public`
- `ecr_public_alias` (optional, default: `aventus`): Public ECR alias

**Migration Steps**:

1. **Update your workflow version**:
   ```yaml
   # Before
   uses: AventusDAO/shared-workflows/.github/workflows/docker-build.yaml@v5.14.0
   
   # After
   uses: AventusDAO/shared-workflows/.github/workflows/docker-build.yaml@v5.15.0
   ```

2. **If using public ECR**, add the new inputs:
   ```yaml
   jobs:
     docker-build:
       uses: AventusDAO/shared-workflows/.github/workflows/docker-build.yaml@v5.15.0
       with:
         ecr_registry_type: "public"
         ecr_public_alias: "your-alias"  # Your public ECR alias
         # ... other inputs
   ```

3. **Agent change** - The default agent is now `arc-ubuntu-2404-x64`. If you need `ubuntu-latest`, explicitly set it:
   ```yaml
   with:
     agent: "ubuntu-latest"  # Explicitly set if needed
     # ... other inputs
   ```

---

## Breaking Changes Summary

### v5.20.0
- ⚠️ **Variable Name Change**: `runner` input renamed to `agent` in `docker-build.yaml` and `check-yarn-application.yml` workflows. Update all references from `runner` to `agent`.

### v5.19.0
- ⚠️ **Terraform Docs Workflow**: Removed hardcoded PR ref checkout. If you need PR-specific checkout, you must now explicitly set `checkout_ref` input.

### v5.18.0
- ⚠️ **Organization Change**: All workflows must reference `AventusDAO` instead of `Aventus-Network-Services`.

### v5.15.0
- ⚠️ **Docker Build**: Default agent changed to `arc-ubuntu-2404-x64`. If your workflows depend on `ubuntu-latest`, you must explicitly set the `agent` input.

---

## Step-by-Step Migration

### Complete Migration from v5.14.0 (or earlier) to v5.20.0

1. **Update Organization References** (if using v5.17.0 or earlier):
   ```bash
   # Find all workflow files
   find .github/workflows -name "*.yml" -o -name "*.yaml" | xargs grep -l "Aventus-Network-Services"
   
   # Replace organization name
   sed -i '' 's/Aventus-Network-Services/AventusDAO/g' .github/workflows/*.yml
   ```

2. **Update Terraform Workflow**:
   ```yaml
   # .github/workflows/terraform.yml
   jobs:
     terraform:
       uses: AventusDAO/shared-workflows/.github/workflows/terraform-workflow.yml@v5.20.0
       # ... rest of config
   ```

3. **Update Terraform Docs Workflow** (if used):
   ```yaml
   # .github/workflows/terraform-docs.yml
   jobs:
     terraform-docs:
       uses: AventusDAO/shared-workflows/.github/workflows/terraform-docs-workflow.yml@v5.20.0
       with:
         checkout_ref: ${{ github.event.pull_request.head.ref }}  # Add if needed for PRs
   ```

4. **Update Terraform Check Workflow**:
   ```yaml
   # .github/workflows/terraform-check.yml
   jobs:
     terraform-check:
       uses: AventusDAO/shared-workflows/.github/workflows/check-workflow.yml@v5.20.0
   ```

5. **Update Docker Build Workflow** (if used):
   ```yaml
   # .github/workflows/docker-build.yml
   jobs:
     docker-build:
       uses: AventusDAO/shared-workflows/.github/workflows/docker-build.yaml@v5.20.0
       with:
         agent: "ubuntu-latest"  # ⚠️ Changed from "runner" to "agent" in v5.20.0
         # ... rest of config
   ```
   
   **Important**: If you were using `runner:` in previous versions, change it to `agent:`.

6. **Test Your Workflows**:
   - Create a test PR to verify workflows run correctly
   - Check that all secrets are properly configured
   - Verify that checkout behavior matches expectations

---

## Version Compatibility Matrix

| Your Current Version | Target Version | Migration Required | Notes |
|---------------------|----------------|-------------------|-------|
| v5.14.0 or earlier | v5.20.0 | ✅ Yes | Organization change + workflow updates |
| v5.15.0 - v5.17.0 | v5.20.0 | ✅ Yes | Organization change + workflow updates |
| v5.18.0 | v5.20.0 | ⚠️ Partial | Only Terraform Docs workflow needs attention |
| v5.19.0 | v5.20.0 | ⚠️ Check | Review v5.20.0 release notes for changes |

---

## Troubleshooting

### Issue: Workflow not found after organization change

**Error**: `Workflow not found: Aventus-Network-Services/shared-workflows/...`

**Solution**: Update all references to use `AventusDAO` instead of `Aventus-Network-Services`.

### Issue: Terraform Docs workflow not checking out PR branch

**Error**: Documentation not updating for PRs

**Solution**: Add `checkout_ref: ${{ github.event.pull_request.head.ref }}` to your workflow inputs.

### Issue: Docker build failing on new agent

**Error**: Build fails on `arc-ubuntu-2404-x64`

**Solution**: Either fix compatibility issues or explicitly set `agent: "ubuntu-latest"`.

### Issue: Workflow input not found after upgrade

**Error**: `Input 'runner' is not defined` or similar errors

**Solution**: Update your workflow inputs from `runner:` to `agent:` in docker-build.yaml and check-yarn-application.yml workflows.

---

## Additional Resources

- [CHANGELOG.md](./CHANGELOG.md) - Complete workflow documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Reusable Workflows Guide](https://docs.github.com/en/actions/using-workflows/reusing-workflows)

---

## Need Help?

If you encounter issues during migration:

1. Check the workflow logs in GitHub Actions
2. Review the [CHANGELOG.md](./CHANGELOG.md) for detailed workflow information
3. Verify your inputs and secrets match the workflow requirements
4. Test in a development branch before updating production workflows

