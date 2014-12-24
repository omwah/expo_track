// Models that should match what the API returns for individual tables

// Adds API class attributes that are just mirrors of
// the data from the server
var make_api_attributes = function(self, data, attributes) {
    for(attr in attributes) {
        attr_name = attributes[attr];
        if (typeof data !== "undefined" && data != null && data[attr_name] !== "undefined") {
            self[attr_name] = ko.observable(data[attr_name]);
        } else {
            self[attr_name] = ko.observable(null);
        }
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

    make_api_attributes(self, data, ["id", "given_name", "family_name", "hidden", "uri"]);

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

    self.member_ids = ko.computed(function() {
        return $.map(self.members(), function(element) {
            return element.id();
        });
    });

    if (data && data.primary_location) {
        self.primary_location = ko.observable(new LocationModel(data.primary_location));
    } else {
        self.primary_location = ko.observable(new LocationModel());
    }

    // This gets pushed to the server on post and put class
    self.primary_location_id = ko.computed(function() {
        if (self.primary_location()) {
            return self.primary_location().id()
        } else {
            return null;
        }
    });
}

function UserModel(data) {
    var self = this;

   var attributes =
        ["id", "name", "uri"];
    make_api_attributes(self, data, attributes);

    self.password = ko.observable(null);

    if(data && data.person) {
        self.person = ko.observable(new PersonModel(data.person));
    } else {
        self.person = ko.observable(new PersonModel());
    }

    self.person_id = ko.computed(function() {
        return self.person().id();
    });

    if (data && data.permissions) {
        self.permissions = ko.observableArray(data.permissions);
    } else {
        self.permissions = ko.observableArray([]);
    }
}
