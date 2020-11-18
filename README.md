# rasa-for-articulate
This project is an example of extending the articulate rasa component.
Using this project, we added new component named `custom_entities` in the rasa 
pipeline.

### Build docker image
```bash
$docker image build -t rasa-for-articulate:latest .
```

### Build image of ner-service
To use the `custom_entities` in the rasa pipeline, you need to build
another docker image using- https://github.com/patelrajnath/ner_service

### Update docker-compose.yml in articulate repository
Change-
```dockerfile
  rasa:
    image: samtecspg/articulate-rasa:1.0.0
    volumes: ["${MODEL_DIR:-./local-storage/rasa/nlu-model}:/app/projects", "${RASA_CONFIG:-./local-storage/rasa/rasa-config.yml}:/app/config.yml", "./local-storage/rasa/logs:/app/logs"]
```
INTO
```dockerfile
  rasa:
    image: rasa-for-articulate:latest
    volumes: ["${MODEL_DIR:-./local-storage/rasa/nlu-model}:/app/projects", "${RASA_CONFIG:-./local-storage/rasa/rasa-config.yml}:/app/config.yml", "./local-storage/rasa/logs:/app/logs"]
```

And add docker-context for ner-service
```dockerfile
ner-service:
    image: ner-service:latest
    container_name: custom-ner
    restart: always
    ports:
      - "9501:9501"
    volumes:
      - ./ner-training:/app/project-ner/training
      - ./ner-training:/app/project-ner/corpus
      - ./ner-training:/app/project-ner/metrics
```

### Add the component in the pipeline
We can enable this component adding the following config in articulate-
```json
  {
    "name": "custom_entities",
    "max_steps": 1000
  }
```
