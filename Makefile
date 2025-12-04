
.PHONY: setup
setup :
	@echo "Setting up the development environment..."
	pyenv virtualenv pingouins || true
	pyenv local pingouins
	pip install -e .
	@echo "✅ Development environment setup complete."

show_config :
	python -m pengouins.config

launch_mlflow :
	@echo "Launching MLflow tracking server..."
	mlflow ui --port $${MLFLOW_LOCAL_PORT:-8888} 
	@echo "✅ MLflow tracking server launched on port $${MLFLOW_LOCAL_PORT:-8888}."


################################################################################################

#						Docker & Deploy

################################################################################################

build : 
	docker build -t ${IMAGE} -f api/Dockerfile .

run : 
	docker run -p ${PORT}:${PORT} -e PORT=${PORT} ${IMAGE}

build_gcp : 
	docker build -t ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE} -f api/Dockerfile .

cloud_build: 
	@echo "submiting build to Google Cloud Build"
	gcloud builds submit .

deploy : 
	gcloud run deploy \
		--image ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE} \
		--region ${LOCATION} \
		--platform managed \
		--allow-unauthenticated
		