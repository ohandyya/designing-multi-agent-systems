.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS=":.*##"; OFS=""; print "\nUsage: make <target>\n"} \
	/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0,5); next } \
	/^[a-zA-Z0-9_.-]+:.*##/ { gsub(/^[[:space:]]+|[[:space:]]+$$/,"",$$2); \
	                          printf "  \033[36m%-28s\033[0m %s\n", $$1, $$2 } \
	END { print "" }' $(MAKEFILE_LIST)

.PHONY: clear
clear:  ## Delete all __pycache__, pytest_cache, and .coverage, and .pymon
	-@find . -name "__pycache__" -o -name ".pytest_cache" -o -name ".coverage" -o -name ".coverage.*"  -o -name ".pymon" | xargs rm -rf

.PHONY: pyright
pyright:  ## Run pyright
	uv run pyright

.PHONY: ruff-check
ruff-check:  ## Run ruff linter check
	uv run ruff check .
	@echo "If you see error, you can auto fix the linter error by running `make ruff-check-fix` "

.PHONY: ruff-check-fix
ruff-check-fix:  ## Run ruff linter check and fix
	uv run ruff check --fix .

.PHONY: ruff-format
ruff-format:  ## Run ruff formatter
	uv run ruff format .


.PHONY: generate-env-script
generate-env-script:	## Generate env script (env.sh)
	@echo "set -a" > env.sh
	@echo "source .env" >> env.sh
	@echo "set +a" >> env.sh
	@chmod +x env.sh
