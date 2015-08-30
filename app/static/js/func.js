function ignoreItem(item_id) {
    alert("Removing: " + item_id);
    $.post("remove/" + item_id, function(data) {
        alert("Ignored");
    });
}
