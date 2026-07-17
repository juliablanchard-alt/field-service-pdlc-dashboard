# Google Service Account Setup for Automated Phase 0 & Phase 1 Data Refresh

This guide explains how to set up a Google Service Account so that GitHub Actions can automatically fetch data from your Google Sheet.

## Overview

The dashboard uses a **GitHub Actions workflow** that runs twice daily (9 AM and 2 PM Pacific Time, Monday-Friday) to:
1. Fetch Phase 0 & Phase 1 data from the Google Sheet using a service account
2. Update `data/phase_0_programs.json`
3. Commit and push the changes to GitHub
4. Heroku automatically deploys the updated data

## Prerequisites

- Admin access to Google Cloud Console
- Admin access to the GitHub repository
- Editor access to the Google Sheet

## Step 1: Create a Google Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Navigate to **IAM & Admin** > **Service Accounts**
4. Click **Create Service Account**
5. Fill in the details:
   - **Name**: `field-service-sheet-reader`
   - **Description**: `Read-only access to Field Service Phase 0 & 1 Google Sheet`
6. Click **Create and Continue**
7. Skip granting roles (we'll use per-sheet permissions)
8. Click **Done**

## Step 2: Create a Service Account Key

1. Click on the newly created service account
2. Go to the **Keys** tab
3. Click **Add Key** > **Create new key**
4. Select **JSON** format
5. Click **Create**
6. The JSON file will download automatically - **keep this file secure!**

The JSON file looks like this:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "field-service-sheet-reader@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

## Step 3: Share the Google Sheet with the Service Account

1. Open the Google Sheet you want to access
2. Click **Share** in the top right
3. Add the service account email (from the JSON file's `client_email` field)
   - Example: `field-service-sheet-reader@your-project.iam.gserviceaccount.com`
4. Set permission to **Viewer** (read-only)
5. Uncheck "Notify people"
6. Click **Share**

## Step 4: Add the Service Account Credentials to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Name: `GOOGLE_SERVICE_ACCOUNT_JSON`
5. Value: Paste the entire contents of the JSON file you downloaded in Step 2
6. Click **Add secret**

## Step 5: Enable GitHub Actions (if needed)

1. In your GitHub repository, go to **Settings** > **Actions** > **General**
2. Under "Workflow permissions", ensure:
   - ✅ Read and write permissions is selected (so the bot can commit)
   - ✅ Allow GitHub Actions to create and approve pull requests (optional)
3. Click **Save**

## Step 6: Test the Workflow

### Option A: Manual Trigger
1. Go to **Actions** tab in GitHub
2. Select "Refresh Phase 0 & Phase 1 Google Sheet Data" workflow
3. Click **Run workflow**
4. Select the branch
5. Click **Run workflow**
6. Watch the workflow execution

### Option B: Wait for Scheduled Run
The workflow runs automatically twice daily:
- 9:00 AM Pacific Time (Monday-Friday)
- 2:00 PM Pacific Time (Monday-Friday)

## Verification

After the workflow runs successfully:
1. Check the **Actions** tab for a green checkmark
2. Verify that `data/phase_0_programs.json` was updated with a new `last_updated` timestamp
3. If Heroku is connected to GitHub, it should automatically deploy the updated data
4. Refresh your dashboard to see the latest Phase 0 & Phase 1 data

## Troubleshooting

### "Error fetching Google Sheet: 403"
- The service account doesn't have access to the sheet
- Go back to Step 3 and ensure the service account email is shared with Viewer permission

### "No service account credentials found"
- The GitHub secret `GOOGLE_SERVICE_ACCOUNT_JSON` is not set or is malformed
- Go back to Step 4 and ensure the entire JSON content is pasted correctly

### "Invalid JSON in GOOGLE_SERVICE_ACCOUNT_JSON"
- The JSON might have been corrupted during copy/paste
- Re-download the key file and paste it again
- Ensure there are no extra characters or line breaks

### Workflow doesn't run automatically
- Check that GitHub Actions is enabled in repository settings
- Verify the cron schedule is correct (times are in UTC)
- Ensure the workflow file is on the `main` branch

## Security Best Practices

1. ✅ **Least Privilege**: Service account only has Viewer access to the specific sheet
2. ✅ **Secrets**: Credentials stored as GitHub encrypted secrets, never in code
3. ✅ **Read-Only**: The service account can only read data, never modify
4. ✅ **Rotation**: If credentials are compromised, revoke the key and create a new one

## Files Involved

- `fetch_phase0_service_account.py` - Python script that fetches data using service account
- `.github/workflows/refresh-phase0-data.yml` - GitHub Actions workflow configuration
- `data/phase_0_programs.json` - Output file (auto-updated by workflow)

## What Data Gets Refreshed?

The workflow fetches from the "Phase 0 & Phase 1 Priorites" tab and includes:
- **PM Backlog (Phase 0)** → Overview tab "PM Backlog" column
- **Prototyping (Phase 1 Col 1)** → Execution tab Phase 1 Column 1
- **Ready for Review (Phase 1 Col 2)** → Execution tab Phase 1 Column 2

All 64+ items are processed with:
- Portfolio assignments
- Program/Product Manager leads
- Status and stage information
- Initiative fallback when Feature is empty
