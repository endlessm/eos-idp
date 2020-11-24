// Facebook Login OAuth redirects the user with an ugly #_=_ URL
// fragment. Strip that off.
//
// https://stackoverflow.com/a/18305085
function stripFacebookOAuthFragment() {
    if (window.location.hash === "#_=_") {
        // If the browser supports history.replaceState, strip the whole
        // fragment. Otherwise just the _=_.
        if (history.replaceState) {
            var noFragment = window.location.href.split("#")[0];
            history.replaceState(null, null, noFragment);
        } else {
            window.location.hash = "";
        }
    }
}

// Strip the fragment immediately after loading.
window.onload = stripFacebookOAuthFragment;
