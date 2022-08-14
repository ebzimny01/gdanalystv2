var th_dict = {
    "G": "G = Game",
    "T": "T = Off Team",
    "Qtr": "Qtr = Quarter",
    "Clk": "Clk = Clock",
    "FP": "FP = Field Position",
    "Dn": "Dn = Down",
    "Dst": "Dst = Distance",
    "OF": "OF = Off Form",
    "DF": "DF = Def Form",
    "DT": "DT = Def Tendency",
    "Blz?": "Blz? = Def Blitz",
    "OT": "OT = Off Play Type",
    "RD": "RD = Run Direction",
    "Prs": "Prs = Def Line Pressure",
    "PD": "PD = Pass Depth",
    "Cvrg": "Cvrg = Def Player Coverage",
    "Cvr": "Cvr = Covered?",
    "PR": "PR = Pass Result",
    "Px": "Px = Pass Extra Detail",
    "Sck": "Sck = Sacked",
    "Pen": "Pen = Penalty",
    "TO": "TO = Turnover",
    "TD": "TD = Touchdown",
    "YG": "YG = Yards Gained",
    "OPM": "OPM = Offensive Play Maker",
    "DPM": "DPM = Defensive Play Maker",
    "PBP": "PBP = Play by Play Text",
    "YPEN": "YPEN = Penalty Yards",
    "Prg": "Prg = QB Progression",
    "Prgx": "Prgx = Prg Details",
    "H": "H = Home Score",
    "A": "A = Away Score",
};

$(document).ready( function () {
    var table = $('#gameresult').DataTable( {
        fixedHeader: true,
        paging: true,
        // "pageLength": 50,
        orderMulti: true,
        order: [[ 2, 'asc' ], [ 3, 'desc' ]],
        responsive: true,
        stateSave: false,
        colReorder: {
            order: [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 28, 29, 17, 18, 19, 20, 21, 22, 23, 27, 24, 25, 26, 30, 31 ]
        },
        dom: 'PBfrtip',
        lengthMenu: [
            [ 50, 100, -1 ],
            [ '50 rows', '100 rows', 'Show all' ]
        ],
        buttons: [
            'pageLength',
            {
                extend: 'colvis',
                collectionLayout: 'fixed two-column',
                columnText: function ( dt, idx, title ) {
                    return th_dict[title];
                },
            },
            'csv', 'excel',
        ],
        searchPanes:{
            columns:[0, 1, 2, 5, 6, 7, 8, 9, 11],
            cascadePanes: true,
            layout: 'columns-9',
        },
        columnDefs:[
            {
                searchPanes:{
                    show: true,
                },
                targets: [0, 1, 2, 5, 6, 7, 8, 9, 11],
            },
            {
                searchPanes:{
                    show: false,
                },
                targets: [3, 4, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
            },
            {
                "visible": false, "targets": [26, 29]
            },
            {
                "width": "300px", "targets": 26,
            },
            { className: "game", "targets": [ 0 ] },
            { className: "team", "targets": [ 1 ] },
            { className: "quarter", "targets": [ 2 ] },
            { className: "clock", "targets": [ 3 ] },
            { className: "fieldposition", "targets": [ 4 ] },
            { className: "down", "targets": [ 5 ] },
            { className: "distance", "targets": [ 6 ] },
            { className: "offenseform", "targets": [ 7 ] },
            { className: "defenseform", "targets": [ 8 ] },
            { className: "deftend", "targets": [ 9 ] },
            { className: "blitz", "targets": [ 10 ] },
            { className: "offtype", "targets": [ 11 ] },
            { className: "rundirection", "targets": [ 12 ] },
            { className: "pressure", "targets": [ 13 ] },
            { className: "passdepth", "targets": [ 14 ] },
            { className: "coverage", "targets": [ 15 ] },
            { className: "covered", "targets": [ 16 ] },
            { className: "passresult", "targets": [ 17 ] },
            { className: "passdetail", "targets": [ 18 ] },
            { className: "sack", "targets": [ 19 ] },
            { className: "penalty", "targets": [ 20 ] },
            { className: "turnover", "targets": [ 21 ] },
            { className: "touchdown", "targets": [ 22 ] },
            { className: "yardsgained", "targets": [ 23 ] },
            { className: "opm", "targets": [ 24 ] },
            { className: "dpm", "targets": [ 25 ] },
            { className: "playbyplay", "targets": [ 26 ] },
            { className: "penaltyyards", "targets": [ 27 ] },
            { className: "progression", "targets": [ 28 ] },
            { className: "progresiondetails", "targets": [ 29 ] },
            { className: "home", "targets": [ 30 ] },
            { className: "away", "targets": [ 31 ] },
        ],
      
        // Add column tooltips
        initComplete: function() {
            $('.game').attr('title', "Game");
            $('.team').attr('title', "Offensive team");
            $('.quarter').attr('title', "Quarter");
            $('.clock').attr('title', "Time on clock");
            $('.fieldposition').attr('title', "Field position");
            $('.down').attr('title', "Down");
            $('.distance').attr('title', "Distance");
            $('.offenseform').attr('title', "Offensive formation");
            $('.defenseform').attr('title', "Defensive formation");
            $('.deftend').attr('title', "Defensive tendency");
            $('.blitz').attr('title', "Blitzing defensive player");
            $('.offtype').attr('title', "Ps = Pass, Rn = Run");
            $('.rundirection').attr('title', "Run Direction");
            $('.pressure').attr('title', "Level of defensive pressure on QB");
            $('.passdepth').attr('title', "Pass depth");
            $('.coverage').attr('title', "Defensive position in pass coverage");
            $('.covered').attr('title', "(C)overed, (W)ell (C)overed, (W)ide (O)pen");
            $('.passresult').attr('title', "(C)omplete or (I)ncomplete pass");
            $('.passdetail').attr('title', "Pass Overthrown, Out of Bounds, Knocked Down");
            $('.sack').attr('title', "Sacked?");
            $('.penalty').attr('title', "Penalty?");
            $('.turnover').attr('title', "Turnover");
            $('.touchdown').attr('title', "Touchdown");
            $('.yardsgained').attr('title', "Yards gained");
            $('.opm').attr('title', "Offensive play maker");
            $('.dpm').attr('title', "Defensive play maker");
            $('.playbyplay').attr('title', "Play by play");
            $('.penaltyyards').attr('title', "Penalty yards");
            $('.progression').attr('title', "QB progression reads");
            $('.progressiondetails').attr('title', "QB progression detailed");
            $('.home').attr('title', "Home team score");
            $('.away').attr('title', "Away team score");
      }
    });
    // $('#gameresult').DataTable().searchPanes.rebuildPane();
    console.log('DOM fully loaded and parsed');
    var x = document.querySelectorAll('.dataTables_scrollBody');
    var i = 0;
    for (i = 0; i < x.length; i++) {
        console.log(x[i]);
        x[i].style.height = "125px";
    }

    var gaugeOptionsDefault = {
        chart: {
          type: 'solidgauge'
        },
      
        title: null,
      
        pane: {
          center: ['50%', '85%'],
          size: '140%',
          startAngle: -90,
          endAngle: 90,
          background: {
            backgroundColor:
              Highcharts.defaultOptions.legend.backgroundColor || '#EEE',
            innerRadius: '60%',
            outerRadius: '100%',
            shape: 'arc'
          }
        },
      
        exporting: {
          enabled: false
        },
      
        tooltip: {
          enabled: false
        },
      
        // the value axis
        yAxis: {
          stops: [
            [0.1, '#55BF3B'], // green
            [0.5, '#DDDF0D'], // yellow
            [0.9, '#DF5353'] // red
          ],
          lineWidth: 0,
          tickWidth: 0,
          minorTickInterval: null,
          tickAmount: 2,
          title: {
            y: -70
          },
          labels: {
            y: 16
          }
        },
      
        plotOptions: {
          solidgauge: {
            dataLabels: {
              y: 5,
              borderWidth: 0,
              useHTML: true
            }
          }
        }
    };

    var gaugeOptionsPass = {
      chart: {
        type: 'solidgauge'
      },
    
      title: null,
    
      pane: {
        center: ['50%', '85%'],
        size: '140%',
        startAngle: -90,
        endAngle: 90,
        background: {
          backgroundColor:
            Highcharts.defaultOptions.legend.backgroundColor || '#EEE',
          innerRadius: '60%',
          outerRadius: '100%',
          shape: 'arc'
        }
      },
    
      exporting: {
        enabled: false
      },
    
      tooltip: {
        enabled: false
      },
    
      // the value axis
      yAxis: {
        stops: [
          [0.3, '#DF5353'], // red
          [0.5, '#DDDF0D'], // yellow
          [0.7, '#55BF3B'] // green
        ],
        lineWidth: 0,
        tickWidth: 0,
        minorTickInterval: null,
        tickAmount: 2,
        title: {
          y: -70
        },
        labels: {
          y: 16
        }
      },
    
      plotOptions: {
        solidgauge: {
          dataLabels: {
            y: 5,
            borderWidth: 0,
            useHTML: true
          }
        }
      }
  };

    var chartRunPass = Highcharts.chart(document.querySelector('#runpasscontainer'), Highcharts.merge(gaugeOptionsDefault, {
        yAxis: {
          min: 0,
          max: 100,
          title: {
            text: 'Run %'
          }
        },
      
        credits: {
          enabled: false
        },
      
        series: [{
          name: 'RunPass',
          data: chartRunPassData(table),
          dataLabels: {
            format:
              '<div style="text-align:center">' +
              '<span style="font-size:40px">{y}</span><br/>' +
              '<span style="font-size:20px;opacity:0.4">% Run Plays</span>' +
              '</div>'
          },
          tooltip: {
            valueSuffix: ' % Run Plays'
          }
        }]
    }));
    
    
    var chartPR = Highcharts.chart(document.querySelector('#passresultcontainer'), Highcharts.merge(gaugeOptionsPass, {
        yAxis: {
          min: 0,
          max: 100,
          title: {
            text: 'Completion %'
          }
        },
      
        credits: {
          enabled: false
        },
      
        series: [{
          name: 'PassResult',
          data: chartPRData(table),
          dataLabels: {
            format:
              '<div style="text-align:center">' +
              '<span style="font-size:40px">{y}</span><br/>' +
              '<span style="font-size:20px;opacity:0.4">% Completion</span>' +
              '</div>'
          },
          tooltip: {
            valueSuffix: ' % Completion'
          }
        }]
    })); 

    var chartBlitz = Highcharts.chart(document.querySelector('#blitzcontainer'), Highcharts.merge(gaugeOptionsDefault, {
        yAxis: {
          min: 0,
          max: 100,
          title: {
            text: 'Blitz %'
          }
        },
      
        credits: {
          enabled: false
        },
      
        series: [{
          name: 'Blitz',
          data: chartBlitzData(table),
          dataLabels: {
            format:
              '<div style="text-align:center">' +
              '<span style="font-size:40px">{y}</span><br/>' +
              '<span style="font-size:20px;opacity:0.4">% Blitz</span>' +
              '</div>'
          },
          tooltip: {
            valueSuffix: ' % Blitz'
          }
        }]
    })); 

    var barchartdata = calculateAverageYardsGained(table);
    var barchartypp = Highcharts.chart(document.querySelector('#yppcontainer'), {
        chart: {
          type: 'column',
          events: {
            drillup: function (e) {
              console.log(this);
              var drillupseriesname = this.options.series[0].name;
              console.log(this.options.series[0].name);
              console.log(this.options.series[0].data[0].name);
              var barchartdata = calculateAverageYardsGained(table);
              this.series.forEach (function (e) {
                if (e.name === drillupseriesname) {
                  e.update({
                    data: [
                      {
                        name: "All Plays",
                        y: barchartdata["yardsperplay"],
                      },
                      {
                        name: "Run Plays",
                        y: barchartdata["yardsperrush"],
                        drilldown: "Run Plays"
                      },
                      {
                        name: "Pass Plays",
                        y: barchartdata["yardsperpass"],
                        drilldown: "Pass Plays"
                      }
                    ]}
                  )
                }
              })
            }
          } 
        },
        title: {
          align: 'left',
          text: 'Yards Per Play'
        },
        subtitle: {
          align: 'left',
          text: 'Click the columns to drill down to run and pass data.'
        },
        accessibility: {
          announceNewData: {
            enabled: true
          }
        },
        xAxis: {
          type: 'category'
        },
        yAxis: {
          title: {
            text: 'Average Yards'
          }
      
        },
        legend: {
          enabled: false
        },
        plotOptions: {
          series: {
            borderWidth: 0,
            dataLabels: {
              enabled: true,
              format: '{point.y:.1f} yds'
            }
          }
        },
      
        tooltip: {
          headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
          pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> yards<br/>'
        },
      
        series: [
          {
            name: "All Plays",
            colorByPoint: true,
            data: [
              {
                name: "All Plays",
                y: barchartdata["yardsperplay"],
              },
              {
                name: "Run Plays",
                y: barchartdata["yardsperrush"],
                drilldown: "Run Plays"
              },
              {
                name: "Pass Plays",
                y: barchartdata["yardsperpass"],
                drilldown: "Pass Plays"
              }
            ]
          }
        ],
        drilldown: {
          breadcrumbs: {
            position: {
              align: 'right'
            }
          },
          series: [
            {
              name: "Run Plays",
              id: "Run Plays",
              data: [
                ["Inside", barchartdata["yardsperrushIn"]],
                ["Outside", barchartdata["yardsperrushOut"]],
                ["QBScr+Sck+Knee", barchartdata["yardsperQBScrSckKneel"]]
              ]
            },
            {
              name: "Pass Plays",
              id: "Pass Plays",
              data: [
                ["Completion", barchartdata["yardspercompletion"]]
              ]
            }
          ]
        }
    });

    // On each draw, update the data in the chart
    table.on('draw', function () {
        var point = chartRunPassData(table);
        console.log('chartRunPassData = ' + point);
        chartRunPass.series[0].points[0].update(point);
        chartPR.series[0].points[0].update(chartPRData(table));
        chartBlitz.series[0].points[0].update(chartBlitzData(table));
        var barchartdata = calculateAverageYardsGained(table);
        //barchartypp.series[0].points[0].update(barchartdata["yardsperplay"]);
        //barchartypp.series[0].points[1].update(barchartdata["yardsperrush"]);
        //barchartypp.series[0].points[2].update(barchartdata["yardsperpass"]);
        // barchartypp.options.drilldrown.series[0].points[0].update(barchartdata["yardsperrushIn"]);
        // barchartypp.options.drilldrown.series[0].points[1].update(barchartdata["yardsperrushOut"]);
        // barchartypp.options.drilldrown.series[0].points[2].update(barchartdata["yardsperQbScrSckKneel"]);
        // barchartypp.options.drilldrown.series[1].points[0].update(barchartdata["yardspercompletion"]);
        // barchartypp.options.drilldrown.series[0].data[0][1] = barchartdata["yardsperrushIn"];
        // barchartypp.options.drilldrown.series[0].data[1][1] = barchartdata["yardsperrushOut"];
        // barchartypp.options.drilldrown.series[0].data[0][2] = barchartdata["yardsperQbScrSckKneel"];
        // barchartypp.options.drilldrown.series[1].data[0][1] = barchartdata["yardspercompletion"];
        
        barchartypp.update({
          drilldown: {
            series: [
              {
                // name: "Run Plays",
                id: "Run Plays",
                data: [
                  ["Inside", barchartdata["yardsperrushIn"]],
                  ["Outside", barchartdata["yardsperrushOut"]],
                  ["QBScr+Sck+Knee", barchartdata["yardsperQBScrSckKneel"]]
                ]
              },
              {
                // name: "Pass Plays",
                id: "Pass Plays",
                data: [
                  ["Completion", barchartdata["yardspercompletion"]]
                ]
              }
            ]
          }
        });
        var ddCurrent = barchartypp.series[0].userOptions.id;
        var ddSeries = barchartypp.options.drilldown.series;
        if (ddCurrent === undefined) {
          // console.log('ddCurrent is undefined');
          // console.log('Current Series Name = ' + barchartypp.series[0].name);
          // console.log('Current Series yData = ' + barchartypp.series[0].yData);
          barchartypp.series[0].setData(barchartypp.options.series[0].data);
          barchartypp.series[0].points[0].update(barchartdata["yardsperplay"]);
          barchartypp.series[0].points[1].update(barchartdata["yardsperrush"]);
          barchartypp.series[0].points[2].update(barchartdata["yardsperpass"]);
        } else {
            for (var i = 0, ie = ddSeries.length; i < ie; ++i) {
              // console.log('ddCurrent = ' + ddCurrent);
              // console.log('ddSeries = ' + ddSeries);
              if (ddSeries[i].id === ddCurrent) {
                // console.log('ddSeries[' + i + '].id = ' + ddSeries[i].id);
                // console.log('ddSeries[' + i + '].data = ' + ddSeries[i].data);
                barchartypp.series[0].setData(ddSeries[i].data);
              }
            }
        }
    });
});


function chartRunPassData(table) {
    var counts = {};
 
    // Count the number of entries for each Offensive Type
    table
        .column(11, { search: 'applied' })
        .data()
        .each(function (val) {
            if (val === '') {
                // do nothing
            } else if (counts[val]) {
                counts[val] += 1;
            } else {
                counts[val] = 1;
            }
        });
 
    // And map it to the format highcharts uses
    if ('Rn' in counts) {
        var runplayspercentage = [Math.round(100 * counts['Rn'] / ((counts['Ps'] || 0) + counts['Rn']))];
    } else {
        var runplayspercentage = [0];
    }
    
    console.log('runplaypercentage = ' + runplayspercentage[0]);
    return runplayspercentage;    
}


function chartPRData(table) {
    var counts = {};
 
    // Count the number of entries for each Pass Result
    table
        .column(19, { search: 'applied' })
        .data()
        .each(function (val) {
            if (val === '') {
                // do nothing
            } else if (counts[val]) {
                counts[val] += 1;
            } else {
                counts[val] = 1;
            }
        });
 
    // And map it to the format highcharts uses
    if ('C' in counts) {
        var passcompletionpercentage = [Math.round(100 * counts['C'] / (counts['C'] + (counts['I'] || 0)))];
    } else {
        var passcompletionpercentage = [0];
    }
    
    console.log('passcompletionpercentage = ' + passcompletionpercentage[0]);
    return passcompletionpercentage;
}

function chartBlitzData(table) {
    var counts = {'No': 0, 'Yes': 0};
 
    // Count the number of entries for each Pass Result
    table
        .column(10, { search: 'applied' })
        .data()
        .each(function (val) {
            // console.log("blitz val = " + val)
            if (val === "") {
                counts['No'] += 1;
            } else {
                counts['Yes'] += 1;
            }
        });
 
    // And map it to the format highcharts uses
    if ('Yes' in counts) {
        var blitzpercentage = [Math.round(100 * counts['Yes'] / (counts['Yes'] + (counts['No'] || 0)))];
    } else {
        var blitzpercentage = [0];
    }
    
    console.log('Blitz No = ' + counts['No']);
    console.log('Blitz Yes = ' + counts['Yes']);
    console.log('Blitz % = ' + blitzpercentage[0]);
    return blitzpercentage;
}


function calculateAverageYardsGained(table) {
    // Array [0] is Off Type
    // Array [1] is Yards Gained
    // Array [2] is Pass Result
    // Array [3] is Run Direction
    var array = table.columns([11,25,19,12], { search: 'applied' }).data();
    console.log(array);
    var playcounter = 0;
    var runplaycounter = 0;
    var runplayINcounter = 0;
    var runplayOUTcounter = 0;
    var runplaySCRcounter = 0;
    var sackplaycounter = 0;
    var qbkneeplaycounter = 0;
    var rushingyardstotal = 0;
    var rushingyardsIN = 0;
    var rushingyardsOUT = 0;
    var rushingyardsSCR = 0;
    var sackyards = 0;
    var qbkneeyards = 0;
    var passplaycounter = 0;
    var passplaycompletecounter = 0;
    var passingyards = 0;
    var counter = 0;
    array[3].forEach(function (x) {
      if (x === 'In') {
        rushingyardsIN += +array[1][counter];
        rushingyardstotal += +array[1][counter];
        runplayINcounter += 1;
        runplaycounter += 1;
      } else if (x === 'Out') {
        rushingyardsOUT += +array[1][counter];
        rushingyardstotal += +array[1][counter];
        runplayOUTcounter += 1;
        runplaycounter += 1;
      } else if (x === 'Scr') {
        rushingyardsSCR += +array[1][counter];
        rushingyardstotal += +array[1][counter];
        runplaySCRcounter += 1;
        runplaycounter += 1;
      } else if (x === 'Sck') {
        sackyards += +array[1][counter];
        rushingyardstotal += +array[1][counter];
        sackplaycounter += 1;
        runplaycounter += 1;
      } else if (x === 'Knee') {
        qbkneeyards += +array[1][counter];
        rushingyardstotal += +array[1][counter];
        qbkneeplaycounter += 1;
        runplaycounter += 1;
      }
      counter += 1;
    });
    counter = 0; // reset counter to parse passing data
    array[2].forEach(function (x) {
      if (x === 'C') {
        passingyards += +array[1][counter];
        passplaycompletecounter += 1;
        passplaycounter += 1;
      } else if (x === 'I') {
        passplaycounter += 1;
      }
      counter += 1;
    });
    playcounter = runplaycounter + passplaycounter;
    let barchartdict = Object.create(null);
    barchartdict["yardsperplay"] = (Math.round(10 * (rushingyardstotal+passingyards)/(runplaycounter+passplaycounter)) / 10) || 0;
    barchartdict["yardsperrush"] = (Math.round(10 * rushingyardstotal/runplaycounter) / 10) || 0;
    barchartdict["yardsperpass"] = (Math.round(10 * passingyards/passplaycounter) / 10) || 0;
    barchartdict["yardsperrushIn"] = (Math.round(10 * rushingyardsIN/runplayINcounter) / 10) || 0;
    barchartdict["yardsperrushOut"] = (Math.round(10 * rushingyardsOUT/runplayOUTcounter) / 10) || 0;
    barchartdict["yardsperQBScrSckKneel"] = (Math.round(10 * (rushingyardsSCR+sackyards+qbkneeyards)/(runplaySCRcounter+sackplaycounter+qbkneeplaycounter)) / 10) || 0;
    barchartdict["yardspercompletion"] = (Math.round(10 * passingyards/passplaycompletecounter) / 10) || 0;
    console.log('Total plays = ' + playcounter + ' | Yards per play = ' + barchartdict["yardsperplay"]);
    console.log('*** RUSHING STATS ***');
    console.log('Inside rushing yards = ' + rushingyardsIN + ' | Inside run plays = ' + runplayINcounter + ' | Inside rushing avg = ' + barchartdict["yardsperrushIn"]);
    console.log('Outside rushing yards = ' + rushingyardsOUT + ' | Outside run plays = ' + runplayOUTcounter + ' | Outside rushing avg = ' + barchartdict["yardsperrushOut"]);
    console.log('QB scramble+sack yards = ' + (rushingyardsSCR + sackyards) + ' | QB scramble+sack plays = ' + (runplaySCRcounter+sackplaycounter) + ' | QB scramble+sack avg = ' + barchartdict["yardsperQBScrSckKneel"]);
    console.log('QB kneel yards = ' + qbkneeyards + ' | QB kneel plays = ' + qbkneeplaycounter);
    console.log('Total rushing yards = ' + rushingyardstotal + ' | Total run plays = ' + runplaycounter + ' | Total rushing avg = ' + barchartdict["yardsperrush"]);
    console.log('*** PASSING STATS ***');
    console.log('Total passing yards = ' + passingyards + ' | Total pass plays = ' + passplaycounter + ' | Yards per pass = ' + barchartdict["yardsperpass"]);
    console.log('Pass completions = ' + passplaycompletecounter + ' | Yards per completion = ' + barchartdict["yardspercompletion"]);
    return barchartdict;
}