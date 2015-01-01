// ------------------
// Login interactions
// ------------------

// div where login interactions occur
var $loginView = $("#login-view");

function AuthViewModel() {
    var self = this;
    self.username = ko.observable();
    self.password = ko.observable();
    self.permissions = ko.observableArray([]);
    self.remember_me = ko.observable();
    self.authenticated = ko.observable(false);

    self.login = function(data) {
        json_request(login_uri, "POST", data).then(
            function(ret_data, textStatus, jqXHR) {
                // .done()
                self.authenticated(true);
                self.password("");
                self.load_permissions();
                $(document).trigger("login");
            },
            function(jqXHR, textStatus, errorThrown) {
                // .failed()
                self.authenticated(false);
                self.password("");
                self.permissions([]);
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
                self.permissions([]);
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
                self.load_permissions();
                $(document).trigger("login");
            },
            function(jqXHR, textStatus, errorThrown) {
                // .failed()
                self.authenticated(false);
                // login view is initially hidden when page is loaded
                self.permissions([]);
                $loginView.removeClass("hidden");
                $(document).trigger("logout");
            }
        );
    }

    self.load_permissions = function() {
        json_request(profile_uri, "GET").done(function(ret_data) {
            self.permissions(ret_data["permissions"]);
        });
    }

}

var auth_view_model = new AuthViewModel();

$( document ).ready(function() {

    // When the page is loaded check if the user still has a valid
    // session cookie for communicating with the server
    auth_view_model.check_auth();

});
