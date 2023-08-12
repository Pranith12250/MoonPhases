from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

# retrieve environment variables
ENDPOINT = os.environ["VISION_TRAINING_ENDPOINT"]
training_key = os.environ["VISION_TRAINING_KEY"]
prediction_key = os.environ["VISION_PREDICTION_KEY"]
prediction_resource_id = os.environ["VISION_PREDICTION_RESOURCE_ID"]

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

publish_iteration_name = "Iteration 1"

# Create a new project
print ("Creating project...")
project_name = 'Moon-phase-trainer'
project = trainer.create_project(project_name)

# Make eight tags in the new project
newmoon_tag = trainer.create_tag(project.id, "New Moon")
waxingcrescent_tag = trainer.create_tag(project.id, "Waxing Crescent")
firstquarter_tag = trainer.create_tag(project.id, "First Quarter")
waxinggibbous_tag = trainer.create_tag(project.id, "Waxing Gibbous")
fullmoon_tag = trainer.create_tag(project.id, "Full Moon")
waninggibbous_tag = trainer.create_tag(project.id, "Waning Gibbous")
thirdquarter_tag = trainer.create_tag(project.id, "Third Quarter")
waningcrescent_tag = trainer.create_tag(project.id, "Waning Crescent")

base_image_location = os.path.join (os.path.dirname(__file__), "Moons")

print("Adding images...")

image_list = []

for image_num in range(1, 6):
    file_name = "New_Moon_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[newmoon_tag.id]))

for image_num in range(1, 10):
    file_name = "Waxing_Crescent_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[waxingcrescent_tag.id]))

for image_num in range(1, 7):
    file_name = "First_Quarter_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[firstquarter_tag.id]))

for image_num in range(1, 13):
    file_name = "Waxing_Gibbous_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[waxinggibbous_tag.id]))

for image_num in range(1, 6):
    file_name = "Full_Moon_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[fullmoon_tag.id]))

for image_num in range(1, 13):
    file_name = "Waning_Gibbous_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[waninggibbous_tag.id]))

for image_num in range(1, 7):
    file_name = "Third_Quarter_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[thirdquarter_tag.id]))

for image_num in range(1, 10):
    file_name = "Waning_Crescent_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[waningcrescent_tag.id]))

upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)

print ("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 10 seconds...")
    time.sleep(10)

# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
print ("Done!")