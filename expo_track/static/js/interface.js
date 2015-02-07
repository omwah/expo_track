// -------------------
// Action interactions
// -------------------

function AddPersonModel(perform) {
    var self = this;

    self.perform = perform;

    self.editing = ko.observable(false);
    self.given_name = ko.observable("");
    self.family_name = ko.observable("");

    self.begin_add = function() {
        self.editing(true);
    }

    self.cancel_add = function() {
        self.editing(false);
        self.given_name("");
        self.family_name("");
    }

    self.finish_add = function() {
        self.editing(false);

        send_data = { given_name: self.given_name(), family_name: self.family_name() };
        json_request(people_uri, "POST", send_data).done(function (ret_data) {
            added_person = new PersonModel(ret_data);
            self.perform.people.push(added_person);
            self.perform.selected_person(added_person.id());

            self.given_name("");
            self.family_name("");
        });

    }
}

function PerformActionModel(all_items) {
    var self = this;

    self.modal_title = ko.observable("");
    self.selected_status = ko.observable("0");
    self.hide_status = ko.observable(false);
    self.selected_item = ko.observable();
    self.hide_items = ko.observable(false);
    self.people = ko.observableArray([]);
    self.selected_person = ko.observable();
    self.modal_loaded = false;

    self.add_person = ko.observable(new AddPersonModel(self));

    self.all_items = all_items;
    self.available_items = ko.computed(function() {
        var curr_status_name = status_types[self.selected_status()];
        return ko.utils.arrayFilter(self.all_items(), function(item) {
            return item.last_action().status() !== curr_status_name;
        });
    });

    self.load_people = function() {
        json_request(people_uri, "GET").done(function(ret_data) {
            var mapped_people = $.map(ret_data, function(person) {
                return new PersonModel(person);
            });
            self.people(mapped_people);
        });
    };

    // Load data from server when page is loaded
    $(document).on("event_loaded", function() {
        self.load_people();
    });

    self.selected_status.subscribe(function() {
        // Only update relevant person when the modal is loaded
        // so we don't call it twice when loading the modal
        //if(self.modal_loaded) {
            self.select_relevant_person();
        //}
    });

    // Select the relevant person who last performed the opposite
    // action of the one that is selected on the item selected
    self.select_relevant_person = function() {
        if(self.selected_item()) {
            var matched_item = ko.utils.arrayFirst(self.all_items(), function(item) {
                if(self.selected_item() == item.id()) {
                    return true;
                }
            });
            self.selected_person(matched_item.last_action().who().id());
        }

       // When used as click handler, allow default event handling
       return true;
    }

    self.begin_action = function(item, sel_status) {
        // Do some additional work when we are given a single item to act upon
        if (item instanceof ItemModel) {
            // Do selected status first as there is a dependency between
            // selected_status and available_items and the form element
            // selected_it does not update properly on first page load
            // unless this is done first. Maybe because available_items is never run,
            // I really don't know why for sure...
            self.selected_status(sel_status);
            self.modal_title(status_command_names[sel_status] + ": " + item.name());
            self.hide_items(true);
            self.hide_status(true)
            self.selected_item(item.id());
            self.selected_item(item.id());
        } else {
            self.selected_status("0");
            self.modal_title("Fast Item Action");
            self.hide_items(false);
            self.hide_status(false);
            if (self.available_items()[0]) {
                self.selected_item(self.available_items()[0].id());
            }
        }

        // Select a person based on the item currently selected
        self.select_relevant_person();

        // If modal was last canceled then cancel any person adding
        self.add_person().cancel_add(false);

        $("#perform-action-modal").modal("show");
        self.modal_loaded = true;
    }

    self.finish_action = function() {
        $("#perform-action-modal").modal("hide");
        self.modal_loaded = false;

        // Save changes to server and update recents list
        action_data = { 'status': self.selected_status(),
                        'person_id': self.selected_person(),
                        'item_id': self.selected_item(),
                        'event_id': base_view_model.event().current().id() }
        json_request(actions_uri, "POST", action_data).done(function(ret_data) {
            created_action = new ActionModel(ret_data); 
            $(document).trigger("item_action", created_action);
        });

    }

}

function ItemDetailsViewModel() {
    var self = this;

    self.modal_title = ko.observable("");
    self.item = ko.observable();

    self.show = function(item) {
        self.item(item);
        self.modal_title("Details for " + item.name());
        $("#item-details-modal").modal("show");
    }
}

function ItemsViewModel(active_status) {
    var self = this;

    self.item_details = ko.observable(new ItemDetailsViewModel());
    
    self.all_items = ko.observableArray([]);
    self.visible_items = ko.computed(function() {
        return ko.utils.arrayFilter(self.all_items(), function(item) {
            return item.last_action().status() === active_status();
        });
    });

    // Create action buttons that will be used in grid for
    // performing item actions. Too many uses of the same word: "action"!
    self.grid_actions = [];

    // Button form bringing up the detailed information screen
    self.grid_actions.push({
        title: "Item Details",
        click: function() {
            self.item_details().show(this);
        },
        icon_class: "fa fa-info fa-fw",
    });

    // For status: Checked In, Checked Out, Missing
    var status_icons = [ "fa fa-download fa-fw", "fa fa-upload fa-fw", "fa fa-question fa-fw" ];
    for (var status_id in status_types) {
        self.grid_actions.push({
            title: status_command_names[status_id],
            click: (function(status_id) {
                return function() {
                    base_view_model.perform().begin_action(this, status_id);
                }
            })(status_id),
            has_permission: (function(status_id) { 
                return function() {
                    return active_status() !== status_types[status_id];
                }
            })(status_id),
            icon_class: status_icons[status_id],
        });
    }

    self.grid_view_model = new ko.sortableGrid.viewModel({
        data: self.visible_items,
        columns: [
            { headerText: "Number", rowText: "tracking_number",
              isSortable: false, rowClass: "col-md-2",
            },
            { headerText: "Name", rowText: "name",
              isSortable: false, rowClass: "col-md-3",
            },
            { headerText: "Description", rowText: "description",
              isSortable: false, rowClass: "col-md-4",
            },         
            { headerText: "Who", rowText: function(item) {
                  return item.last_action().who().display_name();
              },
              isSortable: false, rowClass: "col-md-2",
            },
        ],
        actions: self.grid_actions,
        pageSize: 10,
    });

    self.load = function() {
        self.all_items([]);
        json_request(items_uri, "GET").done(function(ret_data) {
            var mapped_items = $.map(ret_data, function(item) { 
                return new ItemModel(item);
            });
            self.all_items(mapped_items);
        });
    };

    $(document).on("login", function() {
        self.load();
    });

    $(document).on("logout", function() {
        // Clear items on page on logout
        self.all_items([]);
    });

    $(document).on("item_action", function(event, action) {
        // Modify the status of the item who has just had its status change
        var modified_item = ko.utils.arrayFirst(self.all_items(), function(item) {
            return item.name() === action.item();
        });
        modified_item.last_action(action);
    });
}

function ActionsViewModel() {
    var self = this;

    self.recent = ko.observableArray([]);

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

    self.load = function() {
        self.recent([]);
        send_data = { "event_id": base_view_model.event().current().id() }
        json_request(actions_uri, "GET", send_data).done(function(ret_data) {
            var mapped_actions = $.map(ret_data, function(action) { 
                return new ActionModel(action); 
            });
            self.recent(mapped_actions);
        });
    };

    $(document).on("event_loaded", function() {
        self.load();
    });

    $(document).on("logout", function() {
        // Clear actions on page on logout
        self.recent([]);
    });

    $(document).on("item_action", function(event, action) {
        self.recent.unshift(action);
    });

}

function EventViewModel() {
    var self = this;

    self.all = ko.observableArray([]);
    self.current = ko.observable(new EventModel());
    self.selected_id = ko.observable();

    self.load = function() {
        json_request(events_uri, "GET").done(function(ret_data) {
            var mapped_events = $.map(ret_data, function(event) {
                return new EventModel(event);
            });
            self.all(mapped_events);
        });

        var send_data = { soonest: true }
        json_request(events_uri, "GET", send_data).done(function(ret_data) {
            self.current(new EventModel(ret_data[0]));
            $(document).trigger("event_loaded");
        });
    }

    // Hide the switch button normally unless mouse is in the
    // event-info area
    $("#change-event").hide();
    $("#event-info").on("mouseenter", function(e) {
        $("#change-event").show();
    });
    $("#event-info").on("mouseleave", function(e) {
        $("#change-event").hide();
    });

    self.begin_change = function() {
        $("#change-event-modal").modal("show");
        self.selected_id(self.current().id());
    }

    self.end_change = function() {
        $("#change-event-modal").modal("hide");
        var selected_obj = ko.utils.arrayFirst(self.all(), function(event) {
            return event.id() === self.selected_id();
        });
        self.current(selected_obj);
        $(document).trigger("event_loaded");
    }

    return self;
}

// ----------
// Base model
// ----------

function BaseViewModel() {
    var self = this;

    self.tabs = ko.observableArray([]);
    self.active_tab = ko.observable();

    self.auth = ko.observable(auth_view_model);
    self.items = ko.observable(new ItemsViewModel(self.active_tab));
    self.perform = ko.observable(new PerformActionModel(self.items().all_items));
    self.actions = ko.observable(new ActionsViewModel());

    self.event = ko.observable(new EventViewModel());
    
    $(document).on("login", function() {
        // When status def has been loaded then load the tabs for items
        var tabs = [];
        for(var idx in status_types) {
            var status = status_types[idx];
            tabs.push({name: status, title: status})
        }
        tabs.push({name: "actions", title: "Actions Log"})
        self.tabs(tabs);
        self.active_tab(tabs[0].name);
        self.event().load();
    });

    self.active_tab.subscribe(function(new_active) {
        // Reset the page index whenever the active tab changes
        // So that you don't end up with no items shown if one tab
        // does not have the same number of items as another
        self.items().grid_view_model.currentPageIndex(0);
        self.actions().grid_view_model.currentPageIndex(0);
    });

};

var base_view_model = new BaseViewModel();

ko.applyBindings(base_view_model);
