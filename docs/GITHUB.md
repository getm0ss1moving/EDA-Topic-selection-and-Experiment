Current default: human confirmation is optional under the owner's 2026-10-15 instruction. Set repository variable `REQUIRE_HUMAN_FINAL_REPORTS=true` to opt into the distinct-account report review described below. Automated checks and scientific verification always remain required.

# GitHub operations and enforcement

## Enforced gate

`main` requires PRs, resolved conversations, current-base structural checks and status `independent-verifier`. Administrative bypass is disabled by branch protection. Force pushes and deletion are disabled. The bootstrap gate uses GitHub API data only, with no checkout or execution of PR code, and runs from the base branch on `pull_request_target`.

When `REQUIRE_HUMAN_FINAL_REPORTS=true`, final reports under `topics/` and `reports/final/` require account approval. Only accounts explicitly listed in the repository Actions variable `VERIFIER_LOGINS` may confirm. An empty configuration blocks final-report approval. Intermediate PRs require no human review; the unconditional approval count is zero. The review must be `APPROVED`, belong to a different account than the PR author, reference the current full head SHA and contain exactly `CONFIRM <sha>`. A registered verifier's outstanding change request blocks confirmation. All scientific rationale must already exist in files; the review is a transport signal.

A native approval proves account separation, not independent reasoning. The human must verify the session manifest, file packet isolation and verifier's evidence work. All roles using the owner's single GitHub account cannot provide distinct-account human confirmation of final reports. AI scientific independence is established separately by packets and evidence records. Enroll a second GitHub account controlled by the verifier operator or a properly configured review bot; never give a proposer admin credentials for the review identity.

## Enrollment

The owner grants the independent review identity repository access and records its session/operator association in `config/roles.json` by PR. Set `VERIFIER_LOGINS` through repository Settings > Secrets and variables > Actions > Variables (comma-separated GitHub logins). This variable is outside PR-controlled content. Record the change in a run manifest. After enrollment or a variable change, rerun `Independent verifier` with the PR number through workflow dispatch. Removing an identity requires rechecking all open PRs; historical green statuses are not automatically recalculated by a variable change.

If the GitHub account is also the PR author, use a different registered verifier. Do not temporarily disable protection to get a topic through. A human administrator can alter repository settings; GitHub cannot prevent an administrator from changing the rules they administer. Record any such change as a governance incident.

## Routine commands

```sh
git switch -c codex/EDA-0001-proposal
python3 scripts/project.py init EDA-0001
python3 scripts/project.py validate
git add candidates/ runs/
git commit -m "Propose EDA-0001 with evidence and pilot plan"
git push -u origin HEAD
gh pr create --title "EDA-0001: proposed mechanism" --body-file /path/to/pr-body.md
# Independently logged-in verifier, after file-based review:
gh pr review PR_NUMBER --approve --body "CONFIRM FULL_HEAD_SHA"
# Human merge controller, after all checks pass:
gh pr merge PR_NUMBER --squash --delete-branch
```

Do not publish credentials, local private paths or restricted artifacts in the body file. Use the PR template. Structural CI catches omissions and stale hashes, not semantic novelty or truthful evidence. Governance code changes themselves need independent scrutiny.

## References

- [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Secure use of pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)

These references support the GitHub mechanism; research-specific checks are this project's policy.
