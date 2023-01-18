// $(document).ready(function () {
//     var table = $('#variant-table').DataTable({
//         scrollY: '200px',
//         paging: false,
//     });

//     $('#togglers').on('change', function (e) {
//         e.preventDefault();
//         var optionSelected = $("option.toggle-vis:selected", this);
//         var valueSelected = this.value;
//         table.columns().visible( false );

//         // Get the column API object
//         var column = table.column($(this).attr('data-column'));
        
//         // Toggle the visibility
//         column.visible(true);
//     })

// });

$(document).ready(function() {
    var table = $('#variant-table').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            'colvis'
        ]
    });
    table.columns().visible( false );
    $("#variant-table").tabs( {
        "show": function(event, ui) {
            var oTable = $('div.dataTables_scrollBody>table.display', ui.panel).dataTable();
            if ( oTable.length > 0 ) {
                oTable.fnAdjustColumnSizing();
            }
        }
    } );
    $('#togglers').on('change', function (e) {    
        var width = document.getElementById('container').style.offsetWidth;
        if(width > 116)
    });
} );