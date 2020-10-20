const player_lat = document.querySelector('#latitude').innerHTML;
const player_lon = document.querySelector('#longitude').innerHTML;
const playername = document.querySelector('#playername').innerHTML;
const position = document.querySelector('#position').innerHTML;
var mymap = L.map('playermapid').setView([player_lat, player_lon], 5);

var playerIcon = L.icon({
    iconUrl: '/static/gdanalyst/user-solid.svg',
    iconSize:     [26, 62], // size of the icon
    // iconAnchor:   [19, 93], // point of the icon which will correspond to marker's location
    popupAnchor:  [0, -10] // point from which the popup should open relative to the iconAnchor
});

var coachIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

function player_main() {
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiZXplemV6IiwiYSI6ImNrZXN3YjU1aTFwZDAycm1vZWdwYWZ6d3gifQ.xmp7xTHyiB6ZAH4u41Vvow'
    }).addTo(mymap);

    var marker_player = L.marker([player_lat, player_lon], {
        icon: playerIcon,
        title: playername
    }).addTo(mymap);
    marker_player.bindPopup(`${playername} (${position})`);
    var circle_180M_player = L.circle([player_lat, player_lon], {
        color: 'blue',
        fillColor: '#fff',
        fillopacity: 1,
        radius: 290000
    }).addTo(mymap);
    var circle_360M_player = L.circle([player_lat, player_lon], {
        color: 'orange',
        fillColor: '#fff',
        fillopacity: 1,
        radius: 580000
    }).addTo(mymap);
    var circle_1400M_player = L.circle([player_lat, player_lon], {
        color: 'red',
        fillColor: '#fff',
        fillopacity: 1,
        radius: 2250000
    }).addTo(mymap);
}

function markschools() {
    school_list = document.querySelectorAll('.hct');
    school_list.forEach(element => {
        fetch(`/location/${element.id}`)
            .then(response => response.json())
            .then(loc => {
            console.log(loc);
            var marker_player = L.marker([loc[0], loc[1]], {
                icon: coachIcon,
                title: loc[2]
            }).addTo(mymap);
            marker_player.bindPopup(`<a href="\\${element.id}">${loc[2]}</a> (${loc[3]})`);
        });
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
    categories = ['180 miles','360 miles', '1400 miles'];

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

player_main();
markschools();

