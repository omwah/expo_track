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

// -------------------
// Action interactions
// -------------------

function ItemModel(data) {
    var self = this;

    self.id = ko.observable(data.id);
    self.name = ko.observable(data.name);
    self.description = ko.observable(data.description);
    self.status = ko.observable(data.status)
    self.tracking_number = ko.observable(data.tracking_number);
    self.uri = ko.observable(data.uri);
}

function PersonModel(data) {
    var self = this;
    self.id = ko.observable(data.id);
    self.given_name = ko.observable(data.given_name);
    self.family_name = ko.observable(data.family_name);
    self.uri = ko.observable(data.uri);
    self.display_name = ko.computed(function() {
        var given_name = self.given_name();
        var family_name = self.family_name();
        if (family_name !== null && family_name.length > 0) {
            return family_name + ", " + given_name;
        } else {
            return given_name;
        }
    });
}

function ActionItemModel(data) {
    var self = this;

    self.id = ko.observable(data.id);
    self.date = ko.observable(data.date);
    self.item = ko.observable(data.item.name);
    self.status = ko.observable(data.status.name);
    self.who = ko.observable(new PersonModel(data.person));
    self.uri = ko.observable(data.uri);
}

function PerformActionModel() {
    var self = this;

    self.selected_status = ko.observable("0");
    self.available_items = ko.observableArray([]);
    self.selected_item = ko.observableArray([]);
    self.people = ko.observable();
    self.selected_person = ko.observable();

    self.load_items = function() {
        send_data = { "status": self.selected_status() };
        json_request(items_uri, "GET", send_data).done(function(ret_data) {
            var mapped_items = $.map(ret_data, function(item) { 
                return new ItemModel(item); 
            });
            self.available_items(mapped_items);
        });

        // When used as click handler, allow default event handling
        return true;
    };

    self.load_people = function() {
        json_request(people_uri, "GET").done(function(ret_data) {
            var mapped_people = $.map(ret_data, function(person) {
                return new PersonModel(person);
            });
            self.people(mapped_people);
        });

        // When used as click handler, allow default event handling
        return true;
    };
}

var perform_action_model = new PerformActionModel();

function ActionsModel() {
    var self = this;

    self.recent = ko.observableArray([]);
    self.perform = ko.observable(perform_action_model);
    //self.status_types = ko.observableArray([]);

    self.load_recent = function() {
        self.recent([]);
        json_request(actions_uri, "GET").done(function(ret_data) {
            var mapped_actions = $.map(ret_data, function(action) { 
                return new ActionItemModel(action); 
            });
            self.recent(mapped_actions);
        });
    };

    /*self.load_status_types = function() {
        json_request(status_types_uri, "GET").done(function(ret_data) {
            self.status_types(ret_data);
        });
    };*/

    $(document).on("login", function() {
        /*// Keep this loaded on page even after logging out
        if(self.status_types.length == 0) {
            self.load_status_types();
        }*/

        self.load_recent();
    });

    $(document).on("logout", function() {
        // Clear items on page on logout
        self.recent([]);
    });

    self.begin_action = function() {
        $("#perform-action-modal").modal("show");
    }

    self.finish_action = function() {
        $("#perform-action-modal").modal("hide");
    }
}

var actions_model = new ActionsModel();

// ----------
// Base model
// ----------

var base_view_model = function() {
    var self = this;

    self.auth = ko.observable(auth_view_model);
    self.actions = ko.observable(actions_model);
};

ko.applyBindings(base_view_model);

$( document ).ready(function() {

    // When the page is loaded check if the user still has a valid
    // session cookie for communicating with the server
    auth_view_model.check_auth();

});
