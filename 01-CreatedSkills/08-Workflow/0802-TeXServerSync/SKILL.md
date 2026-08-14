---
name: 0802-TeXServerSync
description: Compile TeX projects and upload generated PDFs to a remote server in a fixed two-step order. Use when a user asks to run `compile_tex_file.sh` first and then `upload_pdfs_to_server.sh`, or asks to sync local study PDFs to the configured server after TeX compilation.
---

# Sync TeX And Upload To Server

## Workflow

1. Set the working directory to the repository root that contains both scripts.
2. Confirm `compile_tex_file.sh` and `upload_pdfs_to_server.sh` exist and are executable (or runnable via `bash`).
3. Run `bash compile_tex_file.sh` and wait for completion.
4. If compilation exits non-zero, stop immediately and report the error output.
5. Run `bash upload_pdfs_to_server.sh` only after successful compilation.
6. Report final status for both steps, including failures and the last relevant log lines.

## Command Sequence

Use this exact command order:

```bash
bash compile_tex_file.sh
bash upload_pdfs_to_server.sh
```

Do not reorder, parallelize, or skip steps.

## Fast Execution

For deterministic execution, use the helper script:

```bash
bash scripts/sync_tex_and_upload.sh [repo_root]
```

- If `repo_root` is omitted, run in the current directory.
- The script fails fast when any step fails.
