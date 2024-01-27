// Автоматическая высота у textarea
$(document).on("input", "textarea", function () {
    $(this).outerHeight(134).outerHeight(this.scrollHeight);
});