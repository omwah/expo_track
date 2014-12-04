// ------------------
// Login interactions
// ------------------

// div where login interactions occur
var $loginView = $("#login-view");

function AuthViewModel() {
    var self = this;
    self.username = ko.observable();
    self.password = ko.observable();
    self.remember_me = ko.observable();
    self.authenticated = ko.observable(false);

    self.login = function(data) {
        json_request(login_uri, "POST", data).then(
            function(ret_data, textStatus, jqXHR) {
                // .done()
                self.authenticated(true);
                self.password("");
                $(document).trigger("login");
            },
            function(jqXHR, textStatus, errorThrown) {
                // .failed()
                self.authenticated(false);
                self.password("");
                $(document).trigger("logout");
            }
        );
    }

    self.logout = function(data) {
        json_request(login_uri, "DELETE").done(
            function(ret_data) {
                self.authenticated(false);
                self.username("");
                self.password("");
                // login view is initially hidden when page is loaded
                $loginView.removeClass("hidden");
                $(document).trigger("logout");
            }
        );
    }

    self.check_auth = function() {
        json_request(login_uri, "GET").then(
            function(ret_data, textStatus, jqXHR) {
                // .done()
                self.authenticated(true);
                self.username(ret_data['username']);
                $(document).trigger("login");
            },
            function(jqXHR, textStatus, errorThrown) {
                // .failed()
                self.authenticated(false);
                // login view is initially hidden when page is loaded
                $loginView.removeClass("hidden");
                $(document).trigger("logout");
            }
        );
    }

}

var auth_view_model = new AuthViewModel();

$( document ).ready(function() {

    // When the page is loaded check if the user still has a valid
    // session cookie for communicating with the server
    auth_view_model.check_auth();

});
