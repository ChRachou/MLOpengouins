
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

#						Docker & Deploy — API

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

################################################################################################

#						Docker & Deploy — Front (Streamlit)

################################################################################################

build_front :
	docker build -t ${IMAGE_FRONT} -f front_pengouin/Dockerfile .

run_front :
	docker run -p 8501:8501 ${IMAGE_FRONT}

build_front_gcp :
	@echo "Building Streamlit front image for GCP..."
	docker build -t ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_FRONT} -f front_pengouin/Dockerfile .

cloud_build_front :
	@echo "Submitting Streamlit front build to Google Cloud Build..."
	gcloud builds submit --config=cloudbuild_front.yaml .

deploy_front :
	@echo "Deploying Streamlit front to Cloud Run..."
	gcloud run deploy ${SERVICE_FRONT} \
		--image ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_FRONT} \
		--region ${LOCATION} \
		--platform managed \
		--port 8501 \
		--memory 1Gi \
		--cpu 1 \
		--allow-unauthenticated

		