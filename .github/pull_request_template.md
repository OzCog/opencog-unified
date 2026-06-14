# Pull Request

## Summary

<!--
Describe the change in 2–4 sentences. What problem does it solve, and what
high-level approach was taken? Link to any related issues using `Closes #N`.
-->

Closes #

## Cognitive Layer Affected

- [ ] Foundation (cogutil, moses)
- [ ] Core (atomspace, atomspace-rocks, atomspace-restful)
- [ ] Logic (unify, ure)
- [ ] Cognitive (cogserver, attention, spacetime)
- [ ] Advanced (pln, miner, asmoses)
- [ ] Learning (learn, generate)
- [ ] Language (lg-atomese, relex, link-grammar)
- [ ] Robotics (vision, perception, sensory)
- [ ] Integration (opencog umbrella)
- [ ] CI / Build infrastructure
- [ ] Documentation only

## Engineering Quality Checklist

- [ ] No `TODO`, `FIXME`, or placeholder code introduced (or each is justified inline)
- [ ] All new shell scripts pass `shellcheck`
- [ ] All new YAML files pass `yamllint --strict -c .yamllint.yaml`
- [ ] All new GitHub Actions workflows pass `actionlint -shellcheck=shellcheck`
- [ ] All new Python files pass `ruff check .`
- [ ] No secrets, tokens, or PII added (gitleaks must pass)
- [ ] Public functions / endpoints have docstrings or inline comments
- [ ] Unit tests added or updated where the change affects observable behaviour
- [ ] CHANGELOG / progress notes updated where appropriate

## Test Plan

<!-- How did you verify the change locally? Paste relevant command output. -->

```text
$ <command>
<output>
```

## Risk Assessment

<!--
Briefly note potential blast radius and rollback strategy. For changes to
shared CI infrastructure, list the workflows that may be affected.
-->

- **Blast radius**:
- **Rollback**:

## Reviewer Notes

<!-- Anything you want reviewers to look at first, gotchas, etc. -->
