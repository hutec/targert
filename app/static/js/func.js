function ignoreItem(item_id) {
    alert("Ingoring: " + item_id);
    $.post("/target/ignore/" + item_id, function(data) {
        alert("Ignored");
    });
}

function removeSearch(title) {
    alert("Removing: " + title);
    $.post("/target/remove/" + title, function(data) {
        alert("Removed search");
        window.location.reload();
    });
}


