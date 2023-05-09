(function() {
    var cx = '';
    var gcse = document.createElement('script');
    gcse.async = true;
    gcse.src = 'https://cse.google.com/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
})();

function googleCustomSearchExecute() {
    var input = document.getElementById('cse-search-input-box-id');
    var element = google.search.cse.element.getElement('searchresults-only0');
    if (input.value == '') {
        element.clearAllResults();
    } else {
        element.execute(input.value);
    }
    return false;
}