// Models that should match what the API returns for individual tables

// Adds API class attributes that are just mirrors of
// the data from the server
var make_api_attributes = function(self, data, attributes) {
    for(attr in attributes) {
        attr_name = attributes[attr];
        self[attr_name] = ko.observable(data && data[attr_name] ? data[attr_name] : null);
    }
}

function ItemModel(data) {
    var self = this;

    var attributes =
        ["id", "name", "description", "tracking_number", "uri"];
    make_api_attributes(self, data, attributes);
    self.status = ko.observable(data && data.status ? data.status.name : null);
}

function ContactModel(data) {
    var self = this;

    var attributes =
        ["id", "type", "address", "phone_number", "email_address"];
    make_api_attributes(self, data, attributes);

    if(typeof self.type() === "undefined") {
        self.type(0);
    }
}

function PersonModel(data) {
    var self = this;

    make_api_attributes(self, data, ["id", "given_name", "family_name", "uri"]);

    self.display_name = ko.computed(function() {
        var given_name = self.given_name();
        var family_name = self.family_name();
        if (family_name !== null && family_name.length > 0) {
            return family_name + ", " + given_name;
        } else if (given_name !== null) {
            return given_name;
        }
    });

    if(data && data.contacts) {
        self.contacts = ko.observableArray($.map(data.contacts, function(contact) {
            return new ContactModel(contact);
        }));
    } else {
        self.contacts = ko.observableArray([]);
    }

    self.add_contact = function(data) {
        self.contacts.push(new ContactModel(data));
    };

    self.delete_contact = function() {
        self.contacts.remove(this);
    };
}

function EventModel(data) {
    var self = this;

    var attributes =
        ["id", "name", "description", "uri"];
    make_api_attributes(self, data, attributes);
}

function LocationModel(data) {
    var self = this;

    var attributes =
        ["id", "name", "uri"];
    make_api_attributes(self, data, attributes);

    self.event_id = ko.observable(data && data.event ? data.event.id : null);
}

function TeamModel(data) {
    var self = this;

    var attributes =
        ["id", "name", "uri"];
    make_api_attributes(self, data, attributes);

    if(data && data.members) {
        self.members = ko.observableArray($.map(data.members, function(member) {
            return new PersonModel(member);
        }));
    } else {
        self.members = ko.observableArray([]);
    }

    if (data && data.primary_location) {
        self.primary_location = ko.observable(new LocationModel(data.primary_location));
    } else {
        self.primary_location = ko.observable(new LocationModel());
    }

    // This gets pushed to the server on post and put class
    self.primary_location_id = ko.computed(function() {
        return self.primary_location().id()
    });
}

function UserModel(data) {
    var self = this;

    self.name = ko.observable(data.name);
    self.person = ko.obervable(new PersonModel(data));
    self.permissions = ko.observableArray(data.permissions);
}