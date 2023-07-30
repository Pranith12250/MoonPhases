document.addEventListener('DOMContentLoaded',function()
{
	const uploadButton=document.getElementById('uploadButton');
	const uploadedImage=document.getElementById('uploadedImage');
	const submitButton=document.getElementById('submitButton');

	uploadButton.addEventListener('change',function(event)
	{
		const file=event.target.files[0];
		if(file)
		{
			const reader=new FileReader();
			reader.onload=function(e)
			{
				uploadedImage.src=e.target.result;
				uploadedImage.style.display='block';
				submitButton.removeAttribute('disabled');
			};
			reader.readAsDataURL(file);
		}
	});
});