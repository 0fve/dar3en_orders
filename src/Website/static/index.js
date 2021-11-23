
function Get_color() {
    let current_color = (form.color[form.color.selectedIndex].text);


    // Make a request for a color to check for existing sizes
    axios.get('/checkSizes/' + current_color)
        .then(function (response) {
            let sizes_select = document.getElementById('Size');
            let sizes = ''

            // "of" will show every element while "in" shows the index
            for (var size of response['data']['sizes']) {
                sizes += "<option>"+size+"</option>";
                sizes_select.innerHTML = sizes
            }
        })
}
