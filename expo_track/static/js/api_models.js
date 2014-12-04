// Models that should match what the API returns for individual tables

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
