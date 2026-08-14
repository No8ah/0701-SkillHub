---
name: 0801-PersonalWebsiteDeployment
description: Build and deploy the local personal_website_react Vite/React project to the user's server. Use when the user asks to build personal_website_react, publish the personal website, upload the dist folder, deploy to 8.134.74.103, or update no8ah.cn from the local React site.
---

# Deploy Personal Website

## Workflow

Use the bundled script whenever possible:

```bash
/Users/quzinan/.codex/skills/deploy-personal-website/scripts/deploy.sh
```

The script does all required steps:

1. Runs `npm run build` in `/Users/quzinan/Downloads/Code/personal_website_react`.
2. Packages `dist/` without macOS `._*` metadata files.
3. Uploads the build archive to `root@8.134.74.103`.
4. Extracts it into `/var/www/html`.
5. Cleans stale `assets`, `index.html`, and `resume.pdf` from the previous deployment.
6. Verifies local and remote SHA256 hashes for key files.

## Authentication

Do not hard-code server passwords in this skill.

Prefer existing SSH key authentication. If password login is needed, run the script with `DEPLOY_PASSWORD`:

```bash
DEPLOY_PASSWORD='...' /Users/quzinan/.codex/skills/deploy-personal-website/scripts/deploy.sh
```

## Configuration

Override defaults with environment variables only when the user asks for a different target:

```bash
PROJECT_DIR=/path/to/personal_website_react \
REMOTE_HOST=8.134.74.103 \
REMOTE_USER=root \
REMOTE_DIR=/var/www/html \
/Users/quzinan/.codex/skills/deploy-personal-website/scripts/deploy.sh
```

Default values:

- `PROJECT_DIR=/Users/quzinan/Downloads/Code/personal_website_react`
- `REMOTE_HOST=8.134.74.103`
- `REMOTE_USER=root`
- `REMOTE_DIR=/var/www/html`

## Reporting

After deployment, report:

- Whether `npm run build` passed.
- The remote path updated.
- Whether SHA256 verification passed.
- Any HTTP checks performed, such as `https://no8ah.cn/`.
