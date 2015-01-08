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

function ActionModel(data) {
    var self = this;

    var attributes =
        ["id", "date", "uri"];
    make_api_attributes(self, data, attributes);

    if (data && data.item) {
        self.item = ko.observable(data.item.name);
    } else {
        self.item = ko.observable("");
    }

    if (data && data.status) {
        self.status = ko.observable(data.status.name);
    } else {
        self.status = ko.observable("");
    }

    if (data && data.person) {
        self.who = ko.observable(new PersonModel(data.person));
    } else {
        self.who = ko.observable(null);
    }
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

    self.given_name.extend({required: true});

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

function EventModel(data, date_fmt) {
    var self = this;

    self.date_fmt = date_fmt ? date_fmt : "MM/dd/yyyy";

    var attributes =
        ["id", "name", "description", "begin_date", "end_date", "uri"];
    make_api_attributes(self, data, attributes);

    self.name.extend({required: true});
    self.begin_date.extend({required: true});
    self.end_date.extend({required: true});

    self.format_date = function(date_str) {
        // Backend just gives a date, w/o time, so add time to string
        // so jquery-dateFormat can recognize
        return $.format.date(date_str + "T00:00:00Z", self.date_fmt);
    }

    self.begin_date_fmt = ko.computed(function() {
        return self.format_date(self.begin_date());
    });

    self.end_date_fmt = ko.computed(function() {
        return self.format_date(self.end_date());
    });
}

function LocationModel(data) {
    var self = this;

    var attributes =
        ["id", "name", "uri"];
    make_api_attributes(self, data, attributes);

    self.name.extend({required: true});

    self.event_id = ko.observable(data && data.event ? data.event.id : null);
}

function TeamModel(data) {
    var self = this;

    var attributes =
        ["id", "name", "uri"];
    make_api_attributes(self, data, attributes);

    self.name.extend({required: true});

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

function ItemModel(data) {
    var self = this;

    var attributes =
        ["id", "name", "description", "tracking_number", "uri"];
    make_api_attributes(self, data, attributes);

    self.name.extend({required: true});

    if(data && data.owner) {
        self.owner = ko.observable(new TeamModel(data.owner));
    } else {
        self.owner = ko.observable(null);
    }

    self.owner_id = ko.computed(function() {
        if (self.owner()) {
            return self.owner().id();
        } else {
            return null;
        }
    });

    if (data && data.last_action) {
        self.last_action = ko.observable(new ActionModel(data.last_action));
    } else {
        self.last_action = ko.observable(null);
    }   
}

function UserModel(data) {
    var self = this;

   var attributes =
        ["id", "name", "uri"];
    make_api_attributes(self, data, attributes);

    self.name.extend({required: true});

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
