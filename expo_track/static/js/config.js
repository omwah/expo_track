// ----------
// Handles the configuration logic for the application

// Configure validation
ko.validation.configure({
    messagesOnModified: true,
    // Can not use insertMessages, must add span elements directly
    // as updating the error function on model updates will disconnect
    // the automatically added span from the model
    insertMessages: false,
    messageTemplate: null
});

// Generic interface for communicating with server 
function ApiElementModel(model_type, data) {
    var self = this;

    self.model_type = model_type;
    if (data) {
        self.model = ko.observable(new self.model_type(data));
        self.uri = data.uri;
    } else {
        self.model = ko.observable(new self.model_type());
        self.uri = null;
    }
    self.backup_model = null;

    // Use deep false or else nested classes can cause validation
    // errors
    self.errors = ko.validation.group(self.model, {deep: false});

    // Update error function whenever model changes
    self.model.subscribe(function(updated_model) {
        if(typeof updated_model !== 'undefined') {
            self.errors = ko.validation.group(updated_model, {deep: false});
        }
    });

    // Save a backup of the loaded model in case user cancels and 
    // we can put back what we started with
    self.begin_edit = function() {
        self.load();
        self.backup_model = self.model();
    }

    self.cancel_edit = function() {
        if (self.backup_model != null) {
            self.model(self.backup_model);
        }
        self.backup_model = null;
    }

    self.finish_edit = function() {
        self.update();
        self.backup_model = null;
    }

    // Get data for element from the server
    // Generally just need self.model.id defined
    self.load = function(send_data) {
        if (self.uri) {
            json_request(self.uri, "GET", send_data).done(function(ret_data) {
                self.model(new self.model_type(ret_data));
            });
        }
    }

    // Update data on server from model
    self.update = function() {
        if (self.uri) {
            json_request(self.uri, "PUT", self.model).done(function(ret_data) {
                self.model(new self.model_type(ret_data));
            });
        }
    }

}

function ApiListModel(model_type, columns, perm_suffix, uri) {
    var self = this;

    self.model_type = model_type;
    self.data_elements = ko.observableArray([]);
    self.perm_suffix = perm_suffix;
    self.uri = uri;

    self.edited_item = ko.observable();
    self.editing = ko.observable(false);

    self.can_add = ko.computed(function() {
        return auth_view_model.has_permission("add_" + perm_suffix);
    });

    self.begin_edit = function() {
        // Load full set of data for element
        this.begin_edit();
        self.edited_item(this);
        self.editing(true);
    }

    self.remove = function() {
        var to_remove = this;

        var confirmed;
        if (to_remove.model().name) {
            confirmed = confirm("Are you sure you want to remove: " + to_remove.model().name());
        } else {
            confirmed = confirm("Are you sure you want to remove this element?");
        }

        if (confirmed) {
            json_request(to_remove.uri, "DELETE").done(function(ret_data) {
                self.data_elements.remove(to_remove);
            });
        }
    }

    self.grid_view_model = new ko.sortableGrid.viewModel({
        data: self.data_elements,
        columns: columns,
        pageSize: 10,
        beginEdit: self.begin_edit,
        canEdit: function() { 
            return auth_view_model.has_permission("edit_" + self.perm_suffix) 
        },
        remove: self.remove,
        canRemove: function() { 
            return auth_view_model.has_permission("delete_" + self.perm_suffix) 
        },
    });

    self.load = function(send_data) {
        json_request(self.uri, "GET", send_data).done(function(ret_data) {
            var mapped_elements = $.map(ret_data, function(element) {
                return new ApiElementModel(self.model_type, element);
            });
            self.data_elements(mapped_elements);
        });
    }

    self.begin_new = function() {
        self.edited_item(new ApiElementModel(self.model_type));
        self.editing(true);
    }

    self.cancel_edit = function() {
        self.editing(false);
        self.edited_item().cancel_edit();
        self.edited_item(null);
    }

    self.finish_edit = function() {
        if(self.edited_item().errors().length === 0) {
            self.editing(false);
            if (self.edited_item().uri) {
                self.edited_item().finish_edit();
            } else {
                self.create_new();
            }
            self.edited_item(null);
        } else {
            self.edited_item().errors.showAllMessages();
        }
    }
     
    // Create a new element on the server
    self.create_new = function() {
        var send_data = self.edited_item().model;
        json_request(self.uri, "POST", send_data).done(function(ret_data) {
            self.data_elements.push(new ApiElementModel(self.model_type, ret_data));
        });
    }

    $(document).on("login", function() {
        self.load();
    });

    $(document).on("logout", function() {
        // Clear data
        self.data_elements([]);
    });
}

function ItemsApiListModel() {
    var self = new ApiListModel(ItemModel, 
        [
          { headerText: "Tracking No.", 
            rowText: function(row) { 
                return row.model().tracking_number;
            }, 
            isSortable: true, rowClass: "col-md-2"
          },
          { headerText: "Name",
            rowText: function(row) { 
                return row.model().name;
            },
            isSortable: true, rowClass: "col-md-3",
          },
          { headerText: "Status",
            rowText: function(row) { 
                return row.model().last_action().status;
            }, 
            isSortable: true, rowClass: "col-md-3",
          },
          { headerText: "Owner",
            rowText: function(row) { 
                if (row.model().owner() != null) {
                    return row.model().owner().name;
                } else {
                    return "";
                }
            }, 
            isSortable: true, rowClass: "col-md-3",
          },
        ],
        "item", items_uri);

    self.teams = function() {
        // List of teams with null at the beginning for no associated owner
        var teams = base_view_model.teams().data_elements().slice(0);
        teams.unshift(null);
        return teams;
    }

    self.editing_owner_id = ko.observable();

    self.edited_item.subscribe(function (edited_item) {
        if (edited_item) {
            self.editing_owner_id(edited_item.model().owner().id());
        }
    });

    self.editing_owner_id.subscribe(function(updated_owner_id) {
        var new_owner;
        if(updated_owner_id != null) {
            new_owner = ko.utils.arrayFirst(base_view_model.teams().data_elements(), function(elem) {
                if (elem && elem.model().id() == updated_owner_id) {
                    return true;
                }
            }).model();
        } else {
            new_owner = null;
        }
        self.edited_item().model().owner(new_owner);
    });

    return self;
}

function PeopleApiListModel() {
    var self = new ApiListModel(PersonModel, 
        [
          { headerText: "Name", 
            rowText: function(row) { 
                return row.model().display_name;
            }, 
            isSortable: true, rowClass: "col-md-8"
          },
          { headerText: "Hidden", 
            rowText: function(row) { 
                return row.model().hidden;
            }, 
            isSortable: false, rowClass: "col-md-2"
          },
        ],
        "person",
        // For configuration interface show all people
        people_uri + "?allow_hidden=True");

    return self;
}

function EventsApiListModel() {
    var self = new ApiListModel(EventModel, 
        [
          { headerText: "Name", 
            rowText: function(row) { 
                return row.model().name;
            }, 
            isSortable: true, rowClass: "col-md-7"
          },
          { headerText: "Begin Date", 
            rowText: function(row) { 
                return row.model().begin_date_fmt;
            }, 
            isSortable: true, rowClass: "col-md-2"
          },
          { headerText: "End Date", 
            rowText: function(row) { 
                return row.model().end_date_fmt;
            }, 
            isSortable: true, rowClass: "col-md-2"
          },
        ],
        "event", events_uri);

    self.apply_datepickers = function() {
        // For picking dates and outputting text
        $('.datepicker').datepicker({
            format: "yyyy-mm-dd",
            todayBtn: "linked",
            autoclose: true,
            todayHighlight: true
        });
    }

    // Override begin_edit and begin_new to enable datepickers
    // must be done each time edit is called because HTML
    // is destroyed when edit window goes away
    var parent_begin_new = self.begin_new;
    self.begin_new = function() {
        parent_begin_new();
        self.apply_datepickers();
    }

    var parent_begin_edit = self.begin_edit;
    self.grid_view_model.beginEdit = function() {
        // Use call on parent function so we can
        // pass the correct this object
        parent_begin_edit.call(this);
        self.apply_datepickers();
    }

    return self;
}

function LocationsApiListModel() {
    var self = new ApiListModel(LocationModel, 
        [
          { headerText: "Name", 
            rowText: function(row) { 
                return row.model().name;
            }, 
            isSortable: true, rowClass: "col-md-10"
          },
        ],
        "location", locations_uri);
    return self;
}

function TeamApiListModel() {
    // Extends ApiListModel with mechanisms for the Team interface
    var self = new ApiListModel(TeamModel, 
        [
          { headerText: "Name", 
            rowText: function(row) { 
                return row.model().name;
            }, 
            isSortable: true, rowClass: "col-md-5"
          },
          { headerText: "Primary Location", 
            rowText: function(row) { 
                if (row.model().primary_location() !== null) {
                    return row.model().primary_location().name;
                } else {
                    return "";
                }
            }, 
            isSortable: true, rowClass: "col-md-5"
          },
        ],
        "team", teams_uri);

    self.locations = function() {
        // Locations for teams that includes a null at the beginning
        //
        // Define as a function so it only gets called when the Primary Locations
        // select box gets rendered.
        
        // Copy array into a new one we can modify, using the same objects
        var locations = base_view_model.locations().data_elements().slice(0);

        // Add a null item at the beginning which can be selected if there
        // is no associated location
        locations.unshift(null);
        return locations;
    }
    
    // id of the currently editing model
    self.editing_location_id = ko.observable();

    self.edited_item.subscribe(function (edited_item) {
        // Update the current location id for the options box from
        // the data model
        if (edited_item) {
            self.editing_location_id(edited_item.model().primary_location().id());
        }
    });

    self.editing_location_id.subscribe(function(updated_location_id) {
        // To keep the model consistent, update the primary location object
        // with the correct location object
        if(updated_location_id != self.edited_item().model().primary_location().id()) {
            var new_location;
            if (updated_location_id !== null) {
                new_location = ko.utils.arrayFirst(self.locations(), function(elem) {
                    if (elem && elem.model().id() == updated_location_id) {
                        return true;
                    }
                }).model();
            } else {
                new_location = null;
            }
            self.edited_item().model().primary_location(new_location);
        }
    });

    // Add an observable to stuff the currently selected person when adding team members
    self.added_member_index = ko.observable();

    // Add the selected person to a team
    self.add_team_member = function() {
        var edited_item = this;

        var added_index = self.added_member_index();
        var added_person = base_view_model.people().data_elements()[added_index].model();

        // Make sure we don't have duplicates
        // Need to search our members because if we are adding
        // new people after having saved the member list once the added_person
        // object will be a different one than what is in our members list
        var has_person = ko.utils.arrayFirst(edited_item.model().members(), function(elem) {
            return elem.id() === added_person.id();
        });
        if (!has_person) {
            edited_item.model().members.push(added_person);
        }
    }

    // Remove a team member
    self.remove_team_member = function() {
        self.edited_item().model().members.remove(this);
    }

    return self;
}

function UserApiListModel() {
    var self = new ApiListModel(UserModel, 
        [ { headerText: "User Name", 
            rowText: function(row) { 
                return row.model().name;
            }, 
            isSortable: true, rowClass: "col-md-5"
          },
          { headerText: "Person", 
            rowText: function(row) { 
                return row.model().person().display_name;
            }, 
            isSortable: true, rowClass: "col-md-5"
          },
        ],
        "user", users_uri);

    // Extend load function so we will only load the data
    // with sufficient permissions
    var parent_load = self.load;
    self.load = function() {
        if(auth_view_model.has_permission("view_user")) {
            parent_load();
        }
    }

    // Extend base begin_new with additional functionality
    var parent_begin_new = self.begin_new;
    self.begin_new = function() {
        // Make password required for new users
        parent_begin_new();
        self.edited_item().model().password.extend({required: true});
    }

    // Handle linking drop down of person linked to user and the model
    self.editing_person_id = ko.observable();

    self.edited_item.subscribe(function (edited_item) {
        if (edited_item) {
            self.editing_person_id(edited_item.model().person().id());
        }
    });

    self.editing_person_id.subscribe(function(updated_person_id) {
        if(updated_person_id != null) {
            var new_person = ko.utils.arrayFirst(base_view_model.people().data_elements(), function(elem) {
                if (elem && elem.model().id() == updated_person_id) {
                    return true;
                }
            }).model();

            self.edited_item().model().person(new_person);
        }
    });

    self.check_all_permissions = function(data, event) {
        // Check all permissions on or off according to source checkbox
        var model_permissions = self.edited_item().model().permissions;
        checked = event.target.checked;

        if (checked) {
            // Get name of permissions from the other checkboxes
            var checkboxes = $(event.target).closest("div.row").find(":checkbox");
            ko.utils.arrayForEach(checkboxes, function(item) {
                perm_type = $(item).attr("value");
                if (perm_type && model_permissions().indexOf(perm_type) < 0) {
                    model_permissions.push(perm_type);
                }
            });
        } else {
            model_permissions([]);
        }
        return true;
    };

    return self;
}

function BaseViewModel() {
    var self = this;

    self.auth = ko.observable(auth_view_model);

    self.active_tab = ko.observable("items");
    self.tabs = ko.computed(function() {
        var tabs = [
            { name: "items", title: "Items" },
            { name: "people", title: "People" },
            { name: "events", title: "Events" },
            { name: "locations", title: "Locations" },
            { name: "teams", title: "Teams" },
        ]
        if (self.auth().has_permission("view_user")) {
            tabs.push({ name: "users", title: "Users" });
        }
        return tabs;
    });

    self.items = ko.observable(new ItemsApiListModel());

    self.people = ko.observable(new PeopleApiListModel());

    self.events = ko.observable(new EventsApiListModel());

    self.locations = ko.observable(new LocationsApiListModel());

    self.teams = ko.observable(new TeamApiListModel());
    
    self.users = ko.observable(new UserApiListModel());

    // Client-side routes    
    Sammy(function() {
        // config_base_uri is defined in the html template
        var sammy = this;
        sammy.get(config_base_uri + "#:tab", function() {
            self.active_tab(this.params.tab);
        });
        sammy.get(config_base_uri, function() { this.app.runRoute("get", config_base_uri + "#" + self.tabs()[0].name) });
    }).run();
 
};

var base_view_model = new BaseViewModel();

ko.applyBindings(base_view_model);
