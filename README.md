# rasa-for-articulate
This project is an example of extending the articulate rasa component.
Using this project, we added new component named `custom_entities` in the rasa 
pipeline.

We can enable this component adding the following config in articulate-
```json
  {
    "name": "custom_entities",
    "max_steps": 1000
  }
```

