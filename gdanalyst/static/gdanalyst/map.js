const school_lat = document.querySelector('#latitude').innerHTML;
const school_lon = document.querySelector('#longitude').innerHTML;
const school_name = document.querySelector('#schoolname').innerHTML;
var mymap = L.map('mapid').setView([school_lat, school_lon], 5);

var personIcon = L.icon({
    // iconUrl: 'static/schoolmap/user-solid.svg',
    // iconSize:     [19, 47], // size of the icon
    // iconAnchor:   [10, 46], // point of the icon which will correspond to marker's location
    // popupAnchor:  [-3, -20] // point from which the popup should open relative to the iconAnchor
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

function school_main() {
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiZXplemV6IiwiYSI6ImNrZXN3YjU1aTFwZDAycm1vZWdwYWZ6d3gifQ.xmp7xTHyiB6ZAH4u41Vvow'
    }).addTo(mymap);

    var marker_school = L.marker([school_lat, school_lon], {
        title: school_name
    }).addTo(mymap);
    var circle_180M_school = L.circle([school_lat, school_lon], {
        color: 'blue',
        fillColor: '#fff',
        fillopacity: 1,
        radius: 290000
    }).addTo(mymap);
    var circle_360M_school = L.circle([school_lat, school_lon], {
        color: 'orange',
        fillColor: '#fff',
        fillopacity: 1,
        radius: 580000
    }).addTo(mymap);
    var circle_1400M_player = L.circle([school_lat, school_lon], {
        color: 'red',
        fillColor: '#fff',
        fillopacity: 1,
        radius: 2250000
    }).addTo(mymap);
}

function markschools() {
    school_list = document.querySelectorAll('.hct');
    school_list.forEach(element => {
        sch_short = element.getElementsByClassName('sch_short')[0].innerText;
        sch_coach = element.getElementsByClassName('sch_coach')[0].innerText;        
        sch_lat = element.getElementsByClassName('hct_lat')[0].innerHTML;
        sch_lon = element.getElementsByClassName('hct_lon')[0].innerHTML;
        var marker_school = L.marker([sch_lat, sch_lon], {
            title: sch_short,
            icon: personIcon
        }).addTo(mymap);
        marker_school.bindPopup(`<a href="\\${element.id}">${sch_short}</a> (${sch_coach})`);
        });
}

function getColor(d) {
    return d === '180 miles'  ? 'blue' :
           d === '360 miles'  ? 'orange' :
           d === '1400 miles' ? 'red' :
                                '#FFFFFF';
}

var legend = L.control({position: 'bottomright'});
legend.onAdd = function (mymap) {

    var div = L.DomUtil.create('div', 'info legend');
    labels = ['<strong>Distance</strong>'];
    categories = ['180 miles','360 miles','1400 miles'];

    for (var i = 0; i < categories.length; i++) {

            div.innerHTML += 
            labels.push(
                '<i class="far fa-circle" style="color:' + getColor(categories[i]) + '"></i> ' +
            (categories[i] ? categories[i] : '+'));

        }
        div.innerHTML = labels.join('<br>');
    return div;
};
legend.addTo(mymap);

school_main();
markschools();
