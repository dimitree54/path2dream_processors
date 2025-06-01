# GitHub Secrets Setup Guide

This document explains how to set up the required GitHub Secrets for the CI/CD pipeline to work properly with API integrations.

## Required Secrets

You need to add the following secrets to your GitHub repository:

### API Keys for File Processing

1. **`OPENAI_API_KEY`** - For audio transcription using Whisper
   - Go to: https://platform.openai.com/api-keys
   - Create new API key
   - Copy the key value

2. **`LLAMA_CLOUD_API_KEY`** - For PDF document processing
   - Go to: https://cloud.llamaindex.ai/
   - Sign up/login and generate API key
   - Copy the key value

3. **`JINA_API_KEY`** - For web content extraction
   - Go to: https://jina.ai/
   - Sign up/login and get API key
   - Copy the key value

### CI/CD Pipeline Secrets

4. **`BUMPVERSION_TOKEN`** - For automatic version bumping
   - Go to: https://github.com/settings/personal-access-tokens/new?type=beta
   - Set permission "Contents" to Read & Write
   - Generate token and copy value

5. **`PYPI_PUBLISH_TOKEN`** - For publishing to PyPI
   - Go to: https://pypi.org/manage/account/token/
   - Click "Add API token", set scope for your package
   - Copy the token value

## How to Add Secrets to GitHub

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each secret with the exact name listed above
6. Paste the corresponding value
7. Click **Add secret**

## Testing the Setup

Once all secrets are added:

1. Push your code to the `main` branch
2. Check the **Actions** tab to see if CI/CD runs successfully
3. Verify that integration tests pass with real API calls

## Security Notes

- Never commit API keys to your repository
- Use environment variables or GitHub Secrets only
- Regularly rotate your API keys
- Monitor API usage to detect any unusual activity

## Troubleshooting

If tests fail in CI:

1. Check that all secret names match exactly (case-sensitive)
2. Verify API keys are valid and have sufficient credits
3. Check the Actions logs for specific error messages
4. Ensure your GitHub repository has the correct permissions 