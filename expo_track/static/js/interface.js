// -------------------
// Action interactions
// -------------------

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
    self.selected_item = ko.observable();
    self.people = ko.observable();
    self.selected_person = ko.observable();

    self.load_items = function() {
        // Get the opposite status of the selected status.
        // Ie. If we want to check something in, show the checked out items
        send_data = { "status": base_view_model.opposite_status(self.selected_status()) };
        json_request(items_uri, "GET", send_data).done(function(ret_data) {
            var mapped_items = $.map(ret_data, function(item) { 
                return new ItemModel(item); 
            });
            self.available_items(mapped_items);

            // Set selected as first one, but only if there is an item to pick
            if (self.available_items().length > 0) {
                self.selected_item(self.available_items()[0].id());

                // Select the relevant person for these items
                self.select_relevant_person();
            }
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
    };

    // Select the relevant person who last performed the opposite
    // action of the one that is selected on the item selected
    self.select_relevant_person = function() {
        if(self.selected_item()) {
            send_data = { 
                "status": base_view_model.opposite_status(self.selected_status()),
                "item_id": self.selected_item()
            }

            json_request(actions_uri, "GET", send_data).done(function(ret_data) {
                // Only select a person if the person data coming back is not null.
                // will be null when no person has performed a certain action on an item yet
                if (ret_data.length > 0 && typeof ret_data[0].person !== undefined) {
                    self.selected_person(ret_data[0].person.id);
                } else {
                    self.selected_person(undefined);
                }
            });
        }

        // When used as click handler, allow default event handling
        return true;
    }

    // Load data from server for when modal is newly opened
    self.load_data = function() {
        self.load_items();
        self.load_people();
    }
}

var perform_action_model = new PerformActionModel();

function ActionsModel() {
    var self = this;

    self.recent = ko.observableArray([]);
    self.perform = ko.observable(perform_action_model);

    self.grid_view_model = new ko.sortableGrid.viewModel({
        data: self.recent,
        columns: [
            { headerText: "Date", rowText: function(row) {
                  return $.format.toBrowserTimeZone(row.date());
              },
              isSortable: true, rowClass: "col-md-2",
            },
            { headerText: "Item", rowText: "item",
              isSortable: true, rowClass: "col-md-5",
            },
            { headerText: "Status", rowText: "status",
              isSortable: true, rowClass: "col-md-2",
            },
            { headerText: "Who", rowText: function (row) {
                  return row.who().display_name(); 
              },
              isSortable: true, rowClass: "col-md-3",
            },
        ],
        pageSize: 10,
    });

    self.load_recent = function() {
        self.recent([]);
        json_request(actions_uri, "GET").done(function(ret_data) {
            var mapped_actions = $.map(ret_data, function(action) { 
                return new ActionItemModel(action); 
            });
            self.recent(mapped_actions);
        });
    };

    $(document).on("login", function() {
        self.load_recent();
    });

    $(document).on("logout", function() {
        // Clear items on page on logout
        self.recent([]);
    });

    self.begin_action = function() {
        $("#perform-action-modal").modal("show");

        // Load data each time modal is showed so that
        // it always has fresh data
        perform_action_model.load_data();
    }

    self.finish_action = function() {
        $("#perform-action-modal").modal("hide");

        // Save changes to server and update recents list
        action_data = { 'status': self.perform().selected_status(),
                        'person_id': self.perform().selected_person(),
                        'item_id': self.perform().selected_item(),
                        'event_id': 1 }
        json_request(actions_uri, "POST", action_data).done(function(ret_data) {
            created_action = new ActionItemModel(ret_data); 
            self.recent.unshift(created_action);
        });

    }
}

var actions_model = new ActionsModel();

// ----------
// Base model
// ----------

function BaseViewModel() {
    var self = this;

    self.auth = ko.observable(auth_view_model);
    self.status_def = null;
    self.actions = ko.observable(actions_model);

    self.load_status_def = function() {
        json_request(status_def_uri, "GET").done(function(ret_data) {
            self.status_def = ret_data;
        });
    };

    $(document).on("login", function() {
        // Keep this loaded on page even after logging out
        // and only load it once
        if(self.status_def === null) {
            self.load_status_def();
        }
    });

    self.opposite_status = function(status_code) {
        return self.status_def.opposites[status_code];
    }

};

var base_view_model = new BaseViewModel();

ko.applyBindings(base_view_model);
