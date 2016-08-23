/******************************************************************************
    Point Of Sale - Decimal Numpad Dot
    See README file for full copyright and licensing details.
******************************************************************************/

function pos_numpad_dot_handler(instance, module){

    module.PosWidget.include({

        numpad_handler: function(event){
            if(event.which == 110 && instance.web._t.database.parameters.decimal_point != '.'){
                event.preventDefault();
                event.target.value += instance.web._t.database.parameters.decimal_point;
            }
        },

        start: function() {
            self = this;
            resSuper = this._super();
            res = resSuper.done(function(e){
                document.body.addEventListener('keydown', self.numpad_handler);
            });
            return res;
        },
    });

}

(function(){
    var _super = window.openerp.point_of_sale;
    window.openerp.point_of_sale = function(instance){
        _super(instance);
        var module = instance.point_of_sale;
        pos_numpad_dot_handler(instance, module);
    }
})();
