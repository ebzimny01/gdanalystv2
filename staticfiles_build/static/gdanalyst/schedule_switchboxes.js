const switchAll = document.querySelector('#flexCheckAll');
const switchHumans = document.querySelector('#flexCheckHumans');
const checkboxesAll = document.querySelectorAll('input[name="switch"]');
const checkboxesHumans = document.querySelectorAll('input[name="switch"]:not([value="Sim AI"])');
const btn = document.querySelector('#analyzebtn');
const url = window.location.origin;
const wisid = document.querySelector('div[id="wisid"]').innerHTML;

checkboxesAll.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            btn.disabled = false;
        } else {
            switchAll.checked = false;
            // If any checkboxes remain checked, enable the button, else disable button
            let cbchecked = document.querySelectorAll('input[name="switch"]:checked');
            if (cbchecked.length != 0) {
                btn.disabled = false;
            } else {
                btn.disabled = true;
            }
        }
    });
});

btn.addEventListener('click', () => {
    let checkboxes = document.querySelectorAll('input[name="switch"]:checked');
    let values = [];
    checkboxes.forEach((checkbox) => {
        values.push(checkbox.id);
    });
    var urlquery = url + "/" + wisid + "/schedule/all?";
    values.forEach((item) => {
        urlquery += 'gameids=' + item + "&"
    });
    urlquery = urlquery.slice(0, -1);
    console.log(urlquery);
    window.open(urlquery, '_blank');
});


switchAll.addEventListener('change', () => {
    let checkboxes = document.querySelectorAll('input[name="switch"]');
    if (switchAll.checked) {
        // If Humans is checked, need to change all human checkboxes to checked
        checkboxes.forEach((checkbox) => {
            checkbox.checked = true;
        });
        switchHumans.checked = true;
        btn.disabled = false;
    } else {
        // If Humans is unchecked, need to change all human checkboxes to unchecked
        checkboxes.forEach((checkbox) => {
            checkbox.checked = false;
        });
        switchHumans.checked = false;
        btn.disabled = true;
    }
}); 

switchHumans.addEventListener('change', (event) => {
    let checkboxes = document.querySelectorAll('input[name="switch"]:not([value="Sim AI"])');

    if (switchHumans.checked) {
        // If Humans is checked, need to change all human checkboxes to checked
        checkboxes.forEach((checkbox) => {
            checkbox.checked = true;
        });
        // If all checkboxes are checked, then set All switch to checked
        let cbchecked = document.querySelectorAll('input[name="switch"]:checked');
        if (cbchecked.length === checkboxesAll.length) {
            switchAll.checked = true;
        } else {
            switchAll.checked = false;
        }
        btn.disabled = false;
    } else {
        // If Humans is unchecked, need to change all human checkboxes to unchecked
        checkboxes.forEach((checkbox) => {
            checkbox.checked = false;
        });
        switchAll.checked = false;
        // If any checkboxes remain checked, enable the button, else disable button
        let cbchecked = document.querySelectorAll('input[name="switch"]:checked');
        if (cbchecked.length != 0) {
            btn.disabled = false;
        } else {
            btn.disabled = true;
        }
    }
});


