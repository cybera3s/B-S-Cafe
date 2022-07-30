function createImageSection() {
    /*
        load and validate uploaded image and create its elements
    */
    let file = $(this).prop('files')[0];

    // image type validation
    if (!/image\/*/.test(file.type)) {
        swal(
            'Failed',
            'Wrong type for image input!',
            'error'
        );
        $(this).focus()
        return;
    }
    ;
    // create temporary URl for uploaded file
    let tempURL = URL.createObjectURL(file);
    // create html tags
    let label = `<label for="targetImage">${file.name}</label><br>`
    let img = `<a target="_blank" href="${tempURL}"><img className="rounded" src="${tempURL}" alt="${file.name}" id="targetImage" width="150" height="150"></a>`

    $("#uploadedImage").html(label + img);

};

$('input[type=file]').on('change', createImageSection);