var mymap = L.map('main_mapid').setView([37.09024, -95.712891], 4);

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

var simIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiZXplemV6IiwiYSI6ImNrZXN3YjU1aTFwZDAycm1vZWdwYWZ6d3gifQ.xmp7xTHyiB6ZAH4u41Vvow'
}).addTo(mymap);

function markschools() {
    var markericon;
    school_list = document.querySelectorAll('.hct');
    school_list.forEach(element => {
        fetch(`/location/${element.innerHTML}`)
            .then(response => response.json())
            .then(loc => {
            console.log(loc);
            console.log(loc[3]);
            if (loc[3] === 'Sim AI') {
                markericon = simIcon;
            } else {
                markericon = personIcon;
            }
            var marker_school = L.marker([loc[0], loc[1]], {
                icon: markericon,
                title: loc[2]
            }).addTo(mymap);
            marker_school.bindPopup(`<a href="\\${element.innerHTML}">${loc[2]}</a> (${loc[3]})`);
        });
    });
}

markschools();