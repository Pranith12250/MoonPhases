document.addEventListener('DOMContentLoaded', function() 
{
    const uploadButton = document.getElementById('uploadButton');
    const uploadedImage = document.getElementById('uploadedImage');
    const submitButton = document.getElementById('submitButton');

    fetch('/var/www/config/config.php')
        .then(response => response.text())
        .then(predictionKey => 
        {
            uploadButton.addEventListener('change', function(event) 
            {
                const file = event.target.files[0];
                if (file) 
                {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        uploadedImage.src = e.target.result;
                        uploadedImage.style.display = 'block';
                        submitButton.removeAttribute('disabled');
                    };
                    reader.readAsDataURL(file);
                }
            });

            submitButton.addEventListener('click', function() 
            {
                if (uploadedImage.src && uploadedImage.style.display != 'none') 
                {
                    const image = new Image();
                    image.src = uploadedImage.src;
                    image.onload = function() 
                    {
                        sendImageToPredictionAPI(image, predictionKey);
                    };
                }
            });

            function sendImageToPredictionAPI(image, predictionKey) 
            {
                // const predictionApiUrl = 'https://computervisionlearning2-prediction.cognitiveservices.azure.com/';

                const headers = new Headers(
                {
                    'Prediction-Key': predictionKey,
                    'Content-Type': 'application/octet-stream'
                });

                fetch(image.src)
                    .then(response => response.blob())
                    .then(blob => 
                    {
                        const options = 
                        {
                            method: 'POST',
                            headers: headers,
                            body: blob
                        };

                        fetch('https://computervisionlearning2-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/204d319c-3773-49b0-ab22-0390fca2dd1d/classify/iterations/Iteration2/image', options)
                            .then(response => response.json())
                            .then(data => 
                            {
                                const predictions = data.predictions;
                                let highestProbabilityIndex = 0;
                                for (let i = 1; i < predictions.length; i++) 
                                {
                                    if (predictions[i].probability > predictions[highestProbabilityIndex].probability) 
                                    // {
                                        highestProbabilityIndex = i;
                                    // }
                                }
                                const finalAnswerElement = document.getElementById('finalAnswer');
                                finalAnswerElement.textContent = "Prediction: " + predictions[highestProbabilityIndex].tagName + ", Probability: " + (predictions[highestProbabilityIndex].probability * 100) + "%";
                                finalAnswerElement.style.display = 'block';
                            })
                            .catch(error => 
                            {
                                console.error('Error bro:', error);
                            });
                    })
                    .catch(error => 
                    {
                        console.error('Error fetching image:', error);
                    });
            }

        })
        .catch(error => 
        {
            console.error('Error fetching prediction key:', error);
        });
});