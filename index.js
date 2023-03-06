function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function() {
      var output = document.getElementById('image-preview');
      output.innerHTML = '<img src="' + reader.result + '">';
    }
    reader.readAsDataURL(event.target.files[0]);
}

var fileInput = document.getElementsByName('image')[0];
fileInput.addEventListener('change', previewImage);

function cartoonify_image() {
    const originalImage = document.getElementById("image-preview");

    const imageData = originalImage.src;

    const newImageData = pyodide.runPython(`
    import cv2

    image = cv2.imread('data:image/jpeg;base64,${imageData.split(',')[1]}')
    grayScaleImage= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)
    colorImage = cv2.bilateralFilter(image, 9, 300, 300)
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    _, cartoonImage = cv2.imencode('.jpeg', cartoonImage)
    cartoonImage = cartoonImage.tobytes()
    new_image_data = "data:image/jpeg;base64," + b64encode(cartoon).decode("utf-8")

    new_image_data
`);

originalImage.src = newImageData;
}