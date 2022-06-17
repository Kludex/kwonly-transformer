.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: publish
publish:  ## Publish release to PyPI
	@echo "🔖 Publish to PyPI"
	python setup.py bdist_wheel
	twine upload dist/*
