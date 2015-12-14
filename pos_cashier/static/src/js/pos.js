/******************************************************************************
    Point Of Sale - Cashier selection for Odoo
    See README file for full copyright and licensing details.
******************************************************************************/

openerp.pos_cashier = function (instance){

    // Module initialization
    var module = instance.point_of_sale;

    // Include selection popup CCS style
    $('<link rel="stylesheet" href="/pos_cashier/static/src/css/pos.css"/>').appendTo($("head"));

/* ********************************************************
Extend: point_of_sale.UsernameWidget

- Allow to select cashier by clicking the widget
*********************************************************** */
    module.UsernameWidget.include({

        renderElement: function(){
            var self = this;
            this._super();

            this.$el.click(function(){
                self.click_username();
            });
        },

        click_username: function(){
            var self = this;

            this.select_user().then(function(user) {

                /* set cashier */
                if ( user && user != self.pos.cashier ) {
                    self.pos.cashier = user;
                    self.refresh();
                }
            });
        },

        select_user: function(){
            var self = this;
            var def  = new $.Deferred();

            /* POS user list */
            var userlist = [];
            for (var i = 0; i < this.pos.users.length; i++) {
                var user = this.pos.users[i];

                if(this.pos.config.cashier_list.indexOf(user.id) > -1){
                    userlist.push({
                        'label': user.name,
                        'item':  user,
                    });
                }

            }

            /* Cashier selection popup */
            this.pos.pos_widget.screen_selector.show_popup('select-cashier-popup',{
                'title': 'Cajero',
                list: userlist,
                confirm: function(item){ def.resolve(item); },
            });
            return def.then(function(user){
                return user;
            });

        },

    });

/* ********************************************************
Overload : point_of_sale.PosWidget

- Create and append the new cashier selection widget
*********************************************************** */
    module.PosWidget = module.PosWidget.extend({

        build_widgets: function(){
            this._super();

            this.select_cashier_popup = new module.SelectionCashierWidget(this, {});
            this.select_cashier_popup.appendTo($(this.$el));
            this.screen_selector.popup_set['select-cashier-popup'] = this.select_cashier_popup;
            this.select_cashier_popup.hide();
        },

    });

/* ********************************************************
Define : pos_cashier.SelectionCashierWidget

- This widget displays a pop up to select a cashier (list of enabled users)
*********************************************************** */
    module.SelectionCashierWidget = module.PopUpWidget.extend({

        template:'SelectionCashierWidget',

        show:function(options){
            var self = this;
            options = options || {};
            this._super(options);

            this.title = options.title || ' ';
            this.list = options.list || [];
            this.renderElement();

            this.$('.footer .button').click(function(){
                self.pos_widget.screen_selector.close_popup();
                if ( options.confirm ) {
                    options.confirm.call(self);
                }
            });

            this.$('.selection-item').click(function(event){
                self.pos_widget.screen_selector.close_popup();
                if ( options.confirm ) {
                    var item = self.list[parseInt($(event.target).data('item-index'))];
                    item = item ? item.item : item;
                    options.confirm.call(self,item);
                }
            });
        },

    });

}
