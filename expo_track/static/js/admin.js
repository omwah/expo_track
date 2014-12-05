// ----------
// Base model
// ----------

// Generic interface for communicating with server 
function ApiElementModel(model_type, uri) {
    var self = this;

    self.model_type = model_type;
    self.model = ko.observable(new self.model_type());
    self.uri = uri;

    // Get data for element from the server
    // Generally just need self.model.id defined
    self.get = function(send_data) {
        json_request(self.uri, "GET", send_data).done(function(ret_data) {
            self.model(new self.model_type(ret_data));
        });
    }

    // Create a new element on the server
    self.create = function() {
        json_request(self.uri, "POST", self.model).done(function(ret_data) {
            self.model(new self.model_type(ret_data));
        });
    }

    // Update data on server from model
    self.update = function() {
        json_request(self.uri, "PUT", self.model).done(function(ret_data) {
            self.model(new self.model_type(ret_data));
        });
    }

    // Delete element from server
    // Generally just need self.model.id defined
    self.delete = function() {
        json_request(self.uri, "DELETE").done(function(ret_data) {
            self.model(new self.model_type());
        });
    }
}

function ApiListModel(model_type, uri) {
    var self = this;

    self.model_type = model_type;
    self.data_elements = ko.observableArray([]);
    self.uri = uri;

    self.load = function(send_data) {
        json_request(self.uri, "GET", send_data).done(function(ret_data) {
            var mapped_elements = $.map(ret_data, function(element) {
                return new self.model_type(element);
            });
            self.data_elements(mapped_elements);
        });
    }
    
    $(document).on("login", function() {
        self.load();
    });

    $(document).on("logout", function() {
        self.data_elements([]);
    });
}

function BaseViewModel() {
    var self = this;

    self.auth = ko.observable(auth_view_model);
    self.items = ko.observable(new ApiListModel(ItemModel, items_uri));

};

var base_view_model = new BaseViewModel();

ko.applyBindings(base_view_model);
