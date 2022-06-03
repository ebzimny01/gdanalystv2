function calcRecruitingCost(miles){
    var asstScout = 0;
    var headScout = 0;
    var asstHome = 0;
    var headHome = 0;
    var campus = 0;
    if (miles < 180) {
      asstScout = miles * 0.2041 + 125;
      headScout = miles * 0.3 + 225;
      asstHome = miles * 0.2041 + 400;
      headHome = miles * 0.3 + 500;
      campus = miles * 0.125 + 800;
    } else if (miles >= 180 && miles < 360) {
      asstScout = miles * 0.2 + 200;
      headScout = miles * 0.3 + 300;
      asstHome = miles * 0.2 + 475;
      headHome = miles * 0.3 + 575;
      campus = miles * 0.125 + 1000;
    } else if (miles >= 360 && miles < 1400) {
      asstScout = miles * 0.125 + 460;
      headScout = miles * 0.175 + 560;
      asstHome = miles * 0.125 + 802.6;
      headHome = miles * 0.125 + 1102.6;
      campus = miles * 0.175 + 1200;
    } else if (miles >= 1400 && miles < 2450) {
      asstScout = 700;
      headScout = 1000;
      asstHome = miles * 0.175 + 1070;
      headHome = miles * 0.3 + 1170;
      campus = miles * 0.3 + 1600;
    } else if (miles >= 2450 && miles < 3500) {
      asstScout = 700;
      headScout = 1000;
      asstHome = 1500;
      headHome = miles * 0.3 + 1170;
      campus = miles * 0.3 + 1600;
    } else if (miles >= 3500) {
      asstScout = 700;
      headScout = 1000;
      asstHome = 1500;
      headHome = 2250;
      campus = miles * 0.3 + 1600;
    }
    let costs = [asstScout, headScout,asstHome,headHome,campus];
    return costs;
  };
  
  $(document).ready(function(){
      $("#miles").on('input', function(){
        // Getting the current value of miles input
        var currentMiles = $(this).val();
        let arrayCosts = calcRecruitingCost(currentMiles);
        $("#asstscout").html("$" + Math.floor(arrayCosts[0]));
        $("#headscout").html("$" + Math.floor(arrayCosts[1]));
        $("#assthome").html("$" + Math.floor(arrayCosts[2]));
        $("#headhome").html("$" + Math.floor(arrayCosts[3]));
        $("#campus").html("$" + Math.floor(arrayCosts[4]));
      });
  });