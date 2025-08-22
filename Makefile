.PHONY: help install install-user install-dev test clean build publish

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install for all users (requires sudo)
	pip install -e .

install-user: ## Install for current user only
	pip install --user -e .

install-dev: ## Install with development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	python test_shomei.py

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build distribution packages
	python -m build

publish: ## Publish to PyPI (requires TWINE_USERNAME and TWINE_PASSWORD)
	twine upload dist/*

release: ## Create a new release (usage: make release VERSION=1.0.0)
	@if [ -z "$(VERSION)" ]; then echo "Usage: make release VERSION=1.0.0"; exit 1; fi
	@echo "Creating release v$(VERSION)..."
	git tag -a v$(VERSION) -m "Release v$(VERSION)"
	git push origin v$(VERSION)

install-linux: ## Install on Linux systems
	@echo "Installing shomei on Linux..."
	@echo "1. Installing Python dependencies..."
	sudo apt-get update
	sudo apt-get install -y python3 python3-pip python3-venv git
	@echo "2. Creating virtual environment..."
	python3 -m venv ~/.shomei-env
	@echo "3. Activating environment and installing..."
	. ~/.shomei-env/bin/activate && pip install --upgrade pip && pip install shomei
	@echo "4. Adding to PATH..."
	echo 'export PATH="~/.shomei-env/bin:$$PATH"' >> ~/.bashrc
	@echo "5. Installation complete! Restart your terminal or run: source ~/.bashrc"
	@echo "6. Test with: shomei --help"
