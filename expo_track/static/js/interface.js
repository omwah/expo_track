$( document ).ready(function() {
    var json_request = function(uri, method, data) {
        var request = $.ajax({ url: uri,
                               type: method,
                               contentType: "application/json",
                               accepts: "application/json",
                               cache: false,
                               dataType: "json",
                               data: ko.toJSON(data),
                             });
        return request;
    }

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
                }
            );
        }

        self.check_auth = function() {
            json_request(self.login_uri, "GET").then(
                function(ret_data, textStatus, jqXHR) {
                    // .done()
                    console.log("Am I auth?");
                    self.authenticated(true);
                    self.username(ret_data['username']);
                },
                function(jqXHR, textStatus, errorThrown) {
                    // .failed()
                    self.authenticated(false);
                }
            );
        }

        self.check_auth();
    }
    
    var $loginView = $("#login-view");
    $loginView.hide();
    var loginViewModel = new LoginViewModel();
    ko.applyBindings(loginViewModel);
});
