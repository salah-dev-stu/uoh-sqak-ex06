.PHONY: help test lint check sample replay viewer clean

help:            ## list targets
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/ —/' | sort

test:            ## run the test suite (mocked; no keys/servers)
	uv run pytest

lint:            ## ruff + file-size + version guards
	uv run ruff check .
	uv run python scripts/check_file_lines.py
	uv run python scripts/check_version_sync.py

check: lint test ## all gates

sample:          ## regenerate the committed sample run artifacts
	uv run python scripts/make_sample_run.py

replay: sample   ## rebuild the 3D viewer replay data from the sample
	uv run python scripts/export_replay.py
	@echo "→ refresh the viewer to see the new replay"

viewer:          ## launch the 3D replay theater (static server + open browser)
	uv run python scripts/serve_viewer.py

clean:           ## remove generated run artifacts (keeps committed sample)
	rm -rf reports/runs
