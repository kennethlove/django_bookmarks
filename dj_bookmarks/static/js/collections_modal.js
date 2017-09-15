$('.collection-modal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget);
    var bookmark = button.data('bookmark');
    var modal = $(this);
    modal.find("input[type='hidden']").val(bookmark);
});

$('.collection-modal .btn-primary').on('click', function(event) {
    event.preventDefault();
    var form = $(this).closest('.modal-content').find('form');
    var url = form.attr('action');
    $.ajax(url, {data: form.serialize()})
        .done(function() { $('.collection-modal').modal('hide')})
        .fail(function() { alert("Something went wrong!")})
});
