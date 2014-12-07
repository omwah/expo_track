// Models that should match what the API returns for individual tables

function ItemModel(data) {
    var self = this;

    self.id = ko.observable(data ? data.id : null);
    self.name = ko.observable(data ? data.name : null);
    self.description = ko.observable(data ? data.description : null);
    self.status = ko.observable(data ? data.status.name : null);
    self.tracking_number = ko.observable(data ? data.tracking_number : null);
    // owner 
    self.uri = ko.observable(data ? data.uri : null);
}

function PersonModel(data) {
    var self = this;
    self.id = ko.observable(data ? data.id : null);
    self.given_name = ko.observable(data ? data.given_name : null);
    self.family_name = ko.observable(data ? data.family_name : null);
    self.uri = ko.observable(data ? data.uri : null);
    self.display_name = ko.computed(function() {
        var given_name = self.given_name();
        var family_name = self.family_name();
        if (family_name !== null && family_name.length > 0) {
            return family_name + ", " + given_name;
        } else if (given_name !== null) {
            return given_name;
        }
    });
}

function UserModel(data) {
    var self = this;

    self.name = ko.observable(data.name);
    self.person = ko.obervable(new PersonModel(data));
    self.permissions = ko.observableArray(data.permissions);
}
