// ----------
// Base model
// ----------

function BaseViewModel() {
    var self = this;

    self.auth = ko.observable(auth_view_model);

    $(document).on("login", function() {
    });

};

var base_view_model = new BaseViewModel();

ko.applyBindings(base_view_model);
