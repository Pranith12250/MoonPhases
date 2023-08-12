from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

prediction_key = os.environ["VISION_PREDICTION_KEY"]
prediction_resource_id = os.environ["VISION_PREDICTION_RESOURCE_ID"]
training_key = os.environ["VISION_TRAINING_KEY"]
ENDPOINT = os.environ["VISION_TRAINING_ENDPOINT"]

base_image_location = os.path.join (os.path.dirname(__file__), "Moons")

# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient("https://computervisionlearning2-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/b3292aa6-ced7-48b8-a66e-2677f4f0a931/classify/iterations/classifyModel/image", prediction_credentials)
project_name = 'Moon-phase-trainer'
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
project = trainer.get_project('b3292aa6-ced7-48b8-a66e-2677f4f0a931')
publish_iteration_name = "classifyModel"

with open(os.path.join (base_image_location, "testImage.jpg"), "rb") as image_contents:
    results = predictor.classify_image(project.id, publish_iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))