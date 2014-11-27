// Handle login interactions
$( document ).ready(function() {

    // div where login interactions occur
    var $loginView = $("#login-view");

    function LoginViewModel() {
        var self = this;
        self.username = ko.observable();
        self.password = ko.observable();
        self.remember_me = ko.observable();
        self.authenticated = ko.observable(false);

        self.login_uri = $loginView.find("form")[0].action;

        self.login = function(data) {
            json_request(self.login_uri, "POST", data).then(
                function(ret_data, textStatus, jqXHR) {
                    // .done()
                    self.authenticated(true);
                    self.password("");
                },
                function(jqXHR, textStatus, errorThrown) {
                    // .failed()
                    self.authenticated(false);
                    self.password("");
                }
            );
        }

        self.logout = function(data) {
            json_request(self.login_uri, "DELETE").done(
                function(ret_data) {
                    self.authenticated(false);
                    self.username("");
                    self.password("");
                    // login view is initially hidden when page is loaded
                    $loginView.removeClass("hidden");
                }
            );
        }

        self.check_auth = function() {
            json_request(self.login_uri, "GET").then(
                function(ret_data, textStatus, jqXHR) {
                    // .done()
                    self.authenticated(true);
                    self.username(ret_data['username']);
                },
                function(jqXHR, textStatus, errorThrown) {
                    // .failed()
                    self.authenticated(false);
                    // login view is initially hidden when page is loaded
                    $loginView.removeClass("hidden");
                }
            );
        }

    }
    
    var loginViewModel = new LoginViewModel();

    // When the page is loaded check if the user still has a valid
    // session cookie for communicating with the server
    loginViewModel.check_auth();

    ko.applyBindings(loginViewModel);
});
