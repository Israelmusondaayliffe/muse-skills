---
name: gate-validate
description: "Use when a release gate needs the repo validator run against a clean checkout of the target ref: run the check, parse the JSON, and record the skills count and every error verbatim."
---

Invocation: gate step. The release orchestrator runs this before any install, publish, or sign-off step. Read-only: the validator performs no writes, and the checkout is disposable.

## Inputs

- `REPO_URL`: the repo under review (or a local clone path).
- `TARGET_REF`: the exact branch name or commit SHA under review.
- `WORK_DIR`: scratch directory for the clean checkout.

## Procedure

1. Make a clean checkout of the target ref. Do not reuse a working copy that has local edits.

   ```
   rm -rf "$WORK_DIR/rg-check"
   git clone --depth 1 "$REPO_URL" "$WORK_DIR/rg-check"
   git -C "$WORK_DIR/rg-check" fetch --depth 1 origin "$TARGET_REF"
   git -C "$WORK_DIR/rg-check" checkout --detach "$TARGET_REF"
   git -C "$WORK_DIR/rg-check" status --porcelain
   ```

   The `status --porcelain` output must be empty. If it is not, stop and report a dirty checkout as a gate failure.

2. Run the validator from the checkout root and capture both output streams.

   ```
   python3 tools/validate_collection.py "$WORK_DIR/rg-check" > /tmp/rg-validation.json 2> /tmp/rg-validation.err
   echo "exit=$?"
   ```

3. Parse `/tmp/rg-validation.json`. It has three fields:
   - `skills`: integer count of `skills/*/SKILL.md` files found.
   - `errors`: array of strings, one per problem found.
   - `scope`: string restating what the check covers.

4. Record the skills count and copy every error string verbatim into the gate report. Do not paraphrase errors. Do not drop any.

5. Decide the verdict:
   - PASS only if the script exited 0, the JSON parsed, the `errors` array is empty, and `skills` is greater than 0.
   - FAIL if any error is listed, or if the script itself failed to run: `python3` missing, `tools/validate_collection.py` missing at the repo root, non-JSON output, an exception traceback, or an exit code that does not match the errors array. Copy the stderr verbatim in that case.

6. Do not retry with different flags, and do not edit the checkout to make it pass. Report the checkout as-is.

## What the validator covers

1. Frontmatter, per `skills/*/SKILL.md`: the file must start with YAML frontmatter; `name` must match the parent folder in lowercase-hyphen form; `description` must be present and non-empty.
2. Relative Markdown links: every `[text](path)` in every `.md` file under `skills/`, resolved against the document's own directory, must point to an existing file. Skipped without error: empty links, URLs (contain `:`), absolute paths (start with `/` or `~`), placeholders containing `<>{}*`, and anchor-only fragments.
3. Backtick package paths: inline-code tokens starting with `references/`, `scripts/`, `bin/`, `assets/`, `templates/`, `examples/`, `schemas/`, `../`, or `./` that end with a file extension or a trailing slash must exist either next to the document or at the skill root. Skipped without error: placeholders and globs containing `<>{}*$|`, and non-path tokens such as command output names. The script's `ILLUSTRATIVE_PATHS` map lists confirmed illustrative exceptions (for example, a user-supplied track in one music-video doc). `NOTICE` and `LICENSE` docs are exempt from the backtick check because they name upstream paths, not package files.

## What the validator does NOT cover

- Content quality: prose, prompts, examples, or structure of the skills.
- Upstream fidelity: whether repackaged content matches its original source.
- Whether a skill actually works once installed.
- Whether a linked file is the correct file. The check proves existence only.

## Fail conditions

- FAIL if the `errors` array is non-empty. List every error verbatim in the report.
- FAIL if the script itself failed to run. Record the stderr verbatim.
- A clean validator run is a structural pass only. It says nothing about quality or fidelity.

## Report format

```
Gate: validate
Ref: <target ref>
Skills checked: <n>
Errors: <verbatim list, or "none">
Verdict: PASS | FAIL
```
