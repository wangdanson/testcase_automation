.PHONY: sync-confluence sync-knowledge sync-knowledge-no-sync

sync-confluence:
	python3 sync_from_confluence.py

sync-knowledge:
	python3 sync_knowledge.py

sync-knowledge-no-sync:
	python3 sync_knowledge.py --no-sync
