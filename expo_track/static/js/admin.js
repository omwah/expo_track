// ----------
// Base model
// ----------

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

function ApiListModel(model_type, columns, uri) {
    var self = this;

    self.model_type = model_type;
    self.data_elements = ko.observableArray([]);
    self.uri = uri;
    self.edited_item = ko.observable();
    self.editing = ko.observable(false);
    self.grid_view_model = new ko.sortableGrid.viewModel({
        data: self.data_elements,
        columns: columns,
        pageSize: 10,
        beginEdit: function() {
            // Load full set of data for element
            this.load();
            self.editing(true);
            self.edited_item(this);
        },
        remove: function() {
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
        self.editing(true);
        self.edited_item(new ApiElementModel(self.model_type));
    }

    self.cancel_edit = function() {
        self.editing(false);
        self.edited_item(null);
    }

    self.finish_edit = function() {
        self.editing(false);
        if (self.edited_item().uri) {
            self.edited_item().update();
        } else {
            self.create_new();
        }
        self.edited_item(null);
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

function BaseViewModel() {
    var self = this;

    self.auth = ko.observable(auth_view_model);

    self.active_tab = ko.observable("items");
    self.tabs = ko.observableArray([
            { name: "items", title: "Items" },
            { name: "people", title: "People" },
            { name: "events", title: "Events" },
            { name: "locations", title: "Locations" },
            { name: "teams", title: "Teams" },
    ]);

    self.items = ko.observable(new ApiListModel(ItemModel, 
                 [
                   { headerText: "Tracking No.", 
                     rowText: function(row) { 
                         return row.model().tracking_number }, 
                     isSortable: true, rowClass: "col-md-2"
                   },
                   { headerText: "Name",
                     rowText: function(row) { 
                         return row.model().name },
                     isSortable: true, rowClass: "col-md-6",
                   },
                   { headerText: "Status",
                     rowText: function(row) { 
                         return row.model().status }, 
                     isSortable: true, rowClass: "col-md-3",
                   },
                 ],
                 items_uri));

    self.people = ko.observable(new ApiListModel(PersonModel, 
                 [
                   { headerText: "Name", 
                     rowText: function(row) { 
                         return row.model().display_name }, 
                     isSortable: true, rowClass: "col-md-10"
                   },
                 ],
                 people_uri));

    self.events = ko.observable(new ApiListModel(EventModel, 
                 [
                   { headerText: "Name", 
                     rowText: function(row) { 
                         return row.model().name }, 
                     isSortable: true, rowClass: "col-md-10"
                   },
                 ],
                 events_uri));

    self.locations = ko.observable(new ApiListModel(LocationModel, 
                 [
                   { headerText: "Name", 
                     rowText: function(row) { 
                         return row.model().name }, 
                     isSortable: true, rowClass: "col-md-10"
                   },
                 ],
                 locations_uri));

    self.teams = ko.observable(new ApiListModel(TeamModel, 
                 [
                   { headerText: "Name", 
                     rowText: function(row) { 
                         return row.model().name }, 
                     isSortable: true, rowClass: "col-md-5"
                   },
                   { headerText: "Primary Location", 
                     rowText: function(row) { 
                         return row.model().primary_location().name }, 
                     isSortable: true, rowClass: "col-md-5"
                   },
                 ],
                 teams_uri));

    //$(document).on("login", function() {
    //    // Make sure events are always loaded, since locations depends on it
    //    self['events'].load();
    //});

    // Client-side routes    
    Sammy(function() {
        var sammy = this;
        sammy.get("#:tab", function() {
            self.active_tab(this.params.tab);
        });
        sammy.get('', function() { this.app.runRoute('get', '#' + self.tabs()[0].name) });
    }).run();
 
};

var base_view_model = new BaseViewModel();

ko.applyBindings(base_view_model);
