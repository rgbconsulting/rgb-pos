/******************************************************************************
    Point Of Sale - Cashier selection for Odoo
    See README file for full copyright and licensing details.
******************************************************************************/

openerp.pos_cashier = function (instance){

    // Module initialization
    var module = instance.point_of_sale;
    var _t = instance.web._t;

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
            var current_user = self.pos.cashier || self.pos.user;
            this.select_user(current_user).then(function(user) {

                /* set cashier */
                if ( user && user != self.pos.cashier ) {
                    self.pos.cashier = user;
                    self.refresh();
                }
            });
        },

        select_user: function(current_user){
            var self = this;
            var def  = new $.Deferred();

            /* POS user list */
            var userlist = [];
            for (var i = 0; i < this.pos.users.length; i++) {
                var user = this.pos.users[i];

                if(this.pos.config.cashier_ids.indexOf(user.id) > -1){
                    userlist.push({
                        'label': user.name,
                        'item':  user,
                    });
                }

            }

            /* Cashier selection popup */
            this.pos.pos_widget.screen_selector.show_popup('select-cashier-popup',{
                'title': _t('Change Cashier'),
                list: userlist,
                confirm: function(item){ def.resolve(item); },
            });

            return def.then(function(user){
                if(user){
                    if(user.id !== current_user.id && user.pos_security_pin){
                        return self.ask_password(user.pos_security_pin).then(function(){
                            return user;
                        });
                    } else {
                        return user;
                    }
                }
            });

        },

        ask_password: function(password) {
            var self = this;
            var ret = new $.Deferred();
            if (password) {
                this.pos_widget.screen_selector.show_popup('security-pin',{
                    'title': _t('Security PIN'),
                    confirm: function(pw) {
                        if (pw !== password) {
                            self.pos_widget.screen_selector.show_popup('error-traceback',{
                                message: _t('Incorrect PIN'),
                                comment: _t('The PIN you inserted is incorrect.')
                            });
                            ret.reject();
                        } else {
                            ret.resolve();
                        }
                    },
                });
            } else {
                ret.resolve();
            }
            return ret;
        }

    });


/* ********************************************************
Overload : point_of_sale.PosWidget

- Create and append the new cashier selection widget
*********************************************************** */
    module.PosWidget = module.PosWidget.extend({

        build_widgets: function(){
            this._super();

            // Cashier Popup
            this.select_cashier_popup = new module.SelectionCashierWidget(this, {});
            this.select_cashier_popup.appendTo($(this.$el));
            this.screen_selector.popup_set['select-cashier-popup'] = this.select_cashier_popup;
            this.select_cashier_popup.hide();

            // Security Pin Popup
            this.security_pin_popup = new module.PinPopupWidget(this, {});
            this.security_pin_popup.appendTo($(this.$el));
            this.screen_selector.popup_set['security-pin'] = this.security_pin_popup;
            this.security_pin_popup.hide();
        },

    });


/* ********************************************************
Define : pos_cashier.PinPopupWidget

- Popup widget for cashier security pin
*********************************************************** */
    module.PinPopupWidget = module.PopUpWidget.extend({
        template: 'PinPopupWidget',

        show: function(options){
            var self = this;
            options = options || {};
            this._super(options);
            this.title = options.title || '';
            this.inputbuffer = '' + (options.value   || '');
            this.renderElement();
            this.firstinput = true;

            // Cancel button
            this.$('.button.cancel').click(function(){
                self.hide();
            });

            // Confirm button
            this.$('.button.confirm').click(function(){
                self.pos_widget.screen_selector.close_popup();
                if( options.confirm ){
                    options.confirm.call(self, self.inputbuffer);
                }
            });

            // Input buttons
            this.$('.input-button').click(function(){
                var newbuf = self.numpad_input(
                    self.inputbuffer,
                    $(event.target).data('action'),
                    {'firstinput': self.firstinput}
                );

                self.firstinput = (newbuf.length === 0);

                if (newbuf !== self.inputbuffer) {
                    self.inputbuffer = newbuf;
                    self.$('.value').text(self.inputbuffer);
                }
            });
        },

        numpad_input: function(buffer, input, options) {
            var newbuf  = buffer.slice(0);
            options = options || {};

            if (input === 'CLEAR') {
                newbuf = "";
            } else if (input === 'BACKSPACE') {
                newbuf = newbuf.substring(0,newbuf.length - 1);
            } else if (!isNaN(parseInt(input))) {
                if (options.firstinput) {
                    newbuf = '' + input;
                } else {
                    newbuf += input;
                }
            }

            // End of input buffer at 12 characters.
            if (newbuf.length > buffer.length && newbuf.length > 12) {
                $('body').append('<audio src="/point_of_sale/static/src/sounds/error.wav" autoplay="true"></audio>');
                return buffer.slice(0);
            }

            return newbuf;
        }

    });


/* ********************************************************
Define : pos_cashier.SelectionCashierWidget

- This widget displays a popup to select a cashier (list of enabled users)
*********************************************************** */
    module.SelectionCashierWidget = module.PopUpWidget.extend({

        template:'SelectionCashierWidget',

        show:function(options){
            var self = this;
            options = options || {};
            this._super(options);

            this.title = options.title || '';
            this.list = options.list || [];
            this.renderElement();

            this.$('.footer .button').click(function(){
                self.hide();
            });

            this.$('.selection-item').click(function(event){
                self.hide();
                if ( options.confirm ) {
                    var item = self.list[parseInt($(event.target).data('item-index'))];
                    item = item ? item.item : item;
                    options.confirm.call(self,item);
                }
            });
        },

    });


/* ********************************************************
Overload: point_of_sale.PosModel

- Load extra data needed for cashiers
*********************************************************** */
    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
        self = this;

        // Load cashier security PIN
        for (var i = 0 ; i < this.models.length; i++){
            if (this.models[i].model == 'res.users'){
                this.models[i].fields.push('pos_security_pin');
            }
        }

        return _initialize_.call(this, session, attributes);
    };

}
