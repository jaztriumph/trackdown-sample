function empty() {
    var x;
    x = document.getElementById("id_tagname").value;
    if (x.trim() == "") {
        alert("Tag should not be empty");
        return false;
    }
}

function copyText() {
    Materialize.toast('Link copied', 4000).show();
    var copyText = document.getElementById("link");
    copyText.select();
    document.execCommand("Copy");
    document.getSelection().removeAllRanges();
}

function toastPro() {
    var $toastContent = $('<span>I am toast content</span>').add($('<button class="btn-flat toast-action">Undo</button>'));
    Materialize.toast($toastContent, 10000);

}