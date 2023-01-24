
$(function () {
    var $chk = $("#check-boxes input:checkbox"); // cache the selector
    var $tbl = $('#variant-table').DataTable( {
        dom: 'Bfrtip',
        "pageLength": 50,
        columnDefs: [
            { width: 90, targets: 0 }
        ],
        scrollX:  true,
        'rowsGroup': ['HGNC-Gene-Symbol:name'],
        "language": {
            "zeroRecords": "Veri bulunamadı",  
            "emptyTable":     "Veri bulunamadı",
            "info": "_TOTAL_ sonuçtan _START_-_END_ arası gösteriliyor",
            "infoEmpty": "Sonuç bulunamadı",
            "infoFiltered": "(Toplam sonuç sayısı _MAX_ )",
            "paginate": {
                "next":       "İleri",
                "previous":   "Geri"
            },
            "search":"Arama:",
            "lengthMenu":  " _MENU_ sayfayı göster",
            "loadingRecords": "Yükleniyor...",
            "lengthMenu":   "_MENU_ sonuç gösteriliyor",
        },
        fixedColumns:   {
            left: 1
        }
        });
 
    $chk.prop('checked', false); // uncheck all checkboxes when page loads

    $("#filter-btn").click(function () {
        $tbl.columns().visible( false );
        $("#check-boxes input:checkbox:checked").each(function(){
            var name = $(this).attr("name");
            var col = $tbl.column("." + name);
            col.visible(true); 
        });

        $tbl.column(".variant-link").visible(true);
        $tbl.column(".chrom").visible(true);
        $tbl.column(".pos").visible(true);
        $tbl.column(".ref").visible(true);
        $tbl.column(".alt").visible(true);
        $tbl.column(".HGNC-Gene-Symbol").visible(true);
    });

    $("#filter-btn").click();

    $("#deselect-all-btn").click(function () {
        $chk.prop('checked', false); 
        $tbl.columns().visible(false);

        $tbl.column(".variant-link").visible(true);
        $tbl.column(".chrom").visible(true);
        $tbl.column(".pos").visible(true);
        $tbl.column(".ref").visible(true);
        $tbl.column(".alt").visible(true);
        $tbl.column(".HGNC-Gene-Symbol").visible(true);
    });
});