var th_dict = {
    "T": "T = Off Team",
    "Qtr": "Qtr = Quarter",
    "Clk": "Clk = Clock",
    "FP": "FP = Field Position",
    "Dn": "Dn = Down",
    "Dst": "Dst = Distance",
    "OF": "OF = Off Form",
    "DF": "DF = Def Form",
    "DT": "DT = Def Tendancy",
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
    "H": "H = Home Score",
    "A": "A = Away Score",
};

$(document).ready( function () {
    $('#gameresult').DataTable( {
        fixedHeader: true,
        paging: false,
        orderMulti: true,
        order: [[ 1, 'asc' ], [ 2, 'desc' ]],
        responsive: true,
        stateSave:true,
        colReorder: true,
        dom: 'PBfrtip',
        buttons: [
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
            cascadePanes: false,
            layout: 'columns-8',
        },
        columnDefs:[
            {
                searchPanes:{
                    show: true,
                },
                targets: [0, 1, 4, 5, 6, 7, 8, 10],
            },
            {
                searchPanes:{
                    show: false,
                },
                targets: [2, 3, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
            },
            {
                "visible": false, "targets": 25,
            },
            {
                "width": "300px", "targets": 25,
            }
        ],
    });
    // $('#gameresult').DataTable().searchPanes.rebuildPane();
    console.log('DOM fully loaded and parsed');
    var x = document.querySelectorAll('.dataTables_scrollBody')
    var i = 0
    for (i = 0; i < x.length; i++) {
        console.log(x[i]);
        x[i].style.height = "125px";
    }
} );

/* $(document).ready( function () {
    $('#gameresult').DataTable( {
        fixedHeader: true,
        paging: false,
        orderMulti: true,
        order: [[ 1, 'asc' ], [ 2, 'desc' ]],
        searchPanes:{
            layout: 'columns-9',
            cascadePanes: true
        },
        dom: 'Pfrtip',
        columnDefs:[
            {
                searchPanes:{
                    show: true,
                },
                targets: [0, 1, 4],
            },
            {
                searchPanes:{
                    show: false,
                },
                targets: [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            }
        ],
    });
} ); */