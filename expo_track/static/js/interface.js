$( document ).ready(function() {
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
                },
                function(jqXHR, textStatus, errorThrown) {
                    // .failed()
                    self.authenticated(false);
                    self.password("");
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
                }
            );
        }

        self.check_auth = function() {
            json_request(login_uri, "GET").then(
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

    var auth_view_model = new AuthViewModel();

    // -------------------
    // Action interactions
    // -------------------

    function ActionModel(data) {
        var self = this;

        self.date = ko.observable(data.date);
        self.item = ko.observable(data.item.name);
        self.type = ko.observable(data.type.name);
        self.given_name = ko.observable(data.person.given_name);
        self.family_name = ko.observable(data.person.family_name);
        self.who = ko.computed(function() {
            var given_name = self.given_name();
            var family_name = self.family_name();
            if (family_name.len > 0) {
                return family_name + ", " + given_name;
            } else {
                return given_name;
            }
        });
    }

    function RecentActionsModel() {
        var self = this;

        self.recent_actions = ko.observableArray([]);

        self.load_actions = function() {
            json_request(actions_uri, "GET").done(function(ret_data) {
                var mapped_actions = $.map(ret_data, function(action) { 
                    return new ActionModel(action); 
                });
                self.recent_actions(mapped_actions);
            });
        };
    }

    var recent_actions_model = new RecentActionsModel();

    // ----------
    // Base model
    // ----------

    var base_view_model = function() {
        var self = this;

        self.auth = ko.observable(auth_view_model);
        self.actions = ko.observable(recent_actions_model);
    };

    ko.applyBindings(base_view_model);

    // When the page is loaded check if the user still has a valid
    // session cookie for communicating with the server
    auth_view_model.check_auth();

    recent_actions_model.load_actions();

});
