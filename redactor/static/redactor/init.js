(function($){
    if (!window._redactor_options) window._redactor_options = {};
    $.each(window._redactor_options, function(id, opts) {
        $(id).redactor(opts);
    });
})(window.jQuery || django.jQuery);
