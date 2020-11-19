######################################################################
#  This Dockerfile is used build your Rasa image                     #
######################################################################

# RASA_IMAGE is passed from docker-compose.yml which is generated
# from ./botfront/docker-compose-template.yml and ./botfront/botfront.yml

FROM samtecspg/articulate-rasa:1.0.0

# Change back to root user to install dependencies
USER root

COPY ./extensions/rasa_nlu/registry.py /app/rasa_nlu/
COPY ./extensions/rasa_nlu/extractors/custom_spacy_entity_extractor_remote.py /app/rasa_nlu/extractors/
COPY ./extensions/rasa_nlu/classifiers/ed_classifier.py /app/rasa_nlu/classifiers/

# Switch back to non-root to run code
#USER 1001

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["start", "-c", "config.yml", "--path", "/app/projects"]
