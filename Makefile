.PHONY: setup install-skill run validate sync analyze enrich status

setup:
	./scripts/setup-local.sh

install-skill:
	./scripts/install-codex-skill.sh

run:
	./scripts/run-poi-workflow.sh

validate:
	./scripts/run-poi-workflow.sh --skip-sync --skip-analyze --skip-enrich

sync:
	node scripts/sync-raindrop.mjs

analyze:
	python3 scripts/analyze-poi-videos.py

enrich:
	python3 scripts/enrich-poi-analyses.py

status:
	git status --short
	du -sh raindrop/poi-analysis || true
	find raindrop/poi-analysis -type f -size +50M -print || true
