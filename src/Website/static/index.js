
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
        .catch( function (error){
            location.reload();
        }
        )
}

function enable_edit(){

    let adjustments_inp = document.getElementsByClassName('edit_box')
    let done = document.getElementsByClassName('done')
    for (inp of adjustments_inp){
        console.log(done);
        inp.disabled = false;
        inp.value ='';
    }
};