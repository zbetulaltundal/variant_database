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

} );