
.PHONY: setup
setup :
	@echo "Setting up the development environment..."
	pyenv virtualenv 3.11.8 pingouins
	pyenv local pingouins
	pip install -e .
	@echo "✅ Development environment setup complete."
