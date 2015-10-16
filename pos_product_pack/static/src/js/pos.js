/******************************************************************************
    Point Of Sale - Product packs for Odoo
    See README file for full copyright and licensing details.
******************************************************************************/

openerp.pos_product_pack = function (instance) {

    // Module initialization
    module = instance.point_of_sale;

    // Include CSS style
    $('<link rel="stylesheet" href="/pos_product_pack/static/src/css/pos.css"/>').appendTo($("head"));


/* ********************************************************
Overload: point_of_sale.ProductListWidget

- Add extra behaviour when clicking on a Pack
*********************************************************** */
    module.ProductListWidget = module.ProductListWidget.extend({

        init: function(parent, options) {
            this._super(parent,options);
            var self = this;

            this.click_product_handler = function(event){
                var product = self.pos.db.get_product_by_id(this.dataset['productId']);

                if (!product.is_pack){
                    options.click_product_action(product);
                } else {
                    // Call Pack Popup
                    self.pos.pos_widget.screen_selector.show_popup('product-pack-popup',{
                        'product_pack': product,
                    });
                }
            };
        },

    });


/* ********************************************************
Overload: point_of_sale.PosDB

- Create loaded functions to store the new data
*********************************************************** */
    module.PosDB = module.PosDB.extend({

        init: function(options){
            this.product_pack_lines_by_id = {};
            this._super(options);
        },

        // Store Product Pack Lines
        add_product_pack_lines: function(product_pack_lines){
            for(var i=0 ; i < product_pack_lines.length ; i++){
                this.product_pack_lines_by_id[product_pack_lines[i].id] = product_pack_lines[i];
            }
        },

        // Get list of products from a pack line
        get_products_by_line_id: function(line_id){
            var list = [];
            line = this.product_pack_lines_by_id[line_id];
            for(var i=0 ; i < line.line_product_ids.length ; i++)
            {
                list.push(this.get_product_by_id(line.line_product_ids[i]));
            }
            return list;
        }

    });


/* ********************************************************
Overload: point_of_sale.PosModel

- Load extra data needed for the Pack
*********************************************************** */
    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
        self = this;

        // Load field is_pack and the pack line ids
        for (var i = 0 ; i < this.models.length; i++){
            if (this.models[i].model == 'product.product'){
                this.models[i].fields.push('is_pack','pack_lines_ids');
            }
        }

        // Load Product Pack Lines
        model = {
            model: 'product.pack.line',
            fields: [
                'group_id',
                'line_product_ids',
            ],
            loaded: function(self, values){
                self.db.add_product_pack_lines(values);
            },
        }
        this.models.push(model);

        return _initialize_.call(this, session, attributes);
    };


/* ********************************************************
Define: point_of_sale.ProductPackPopup

- This widget will display a popup to configure the pack
*********************************************************** */
    module.ProductPackPopup = module.PopUpWidget.extend({
        template:'ProductPackPopup',

        start: function(){
            self = this;
            this.current_group = 0;
            var product_pack;
            this.selected_products = [];

            // Initialize ProductListWidget with empty product list
            this.product_list_widget = new module.ProductListWidget(this,{
                click_product_action: function(product){
                    self.selected_products.push(product);
                    self.show_product_group_pack();
                },
                product_list: []
            });
            this.product_list_widget.replace(this.$('.placeholder-ProductListWidget'));
        },

        show:function(options){
            var self = this;
            options = options || {};

            self.product_pack = options.product_pack;
            this._super(options);
            this.$('#pack-name').html(self.product_pack.display_name);
            this.show_product_group_pack();

            this.$('.footer .button').click(function(){
                self.clear_popup();
            });
        },

        show_product_group_pack: function(){
            var self = this;
            // Check for next group and list it if exists
            if(self.current_group < self.product_pack.pack_lines_ids.length){
                this.$('#group-name').html(self.pos.db.product_pack_lines_by_id[self.product_pack.pack_lines_ids[self.current_group]].group_id[1]);
                self.product_list_widget.set_product_list(this.pos.db.get_products_by_line_id(self.product_pack.pack_lines_ids[self.current_group]))
                self.current_group +=1;
            }
            else
            {
                this.add_products_to_order(self.product_pack,self.selected_products);
                this.clear_popup();
            }
        },

        // Add products from pack to POS Order
        add_products_to_order: function(pack,products){
            var self = this;
            var code = 'pack-' + pack.id + '-' + new Date().getTime();
            self.pos.get('selectedOrder').addProduct(pack, {'is_pack_container':1, 'pack_code': code});
            for(var i=0 ; i < products.length ; i++){
                self.pos.get('selectedOrder').addProduct(products[i], {'is_pack_item':1, 'pack_code': code, 'discount': 100});
            }
        },

        // Clear the popup
        clear_popup: function(){
            var self = this;
            self.current_group = 0;
            self.product_pack = null;
            self.selected_products = [];
            self.pos_widget.screen_selector.close_popup();
        }

    });


/* ********************************************************
Overload : point_of_sale.Order

- Change behaviour of addProduct for pack products
*********************************************************** */
    var OrderSuper = module.Order;
    module.Order = module.Order.extend({

        addProduct: function(product, options){
            options = options || {}
            if (options.pack_code){
                product = $.extend({'is_pack_item': options.is_pack_item,
                                    'is_pack_container': options.is_pack_container,
                                    'pack_code': options.pack_code
                                   },
                                   JSON.parse(JSON.stringify(product)));
                if (options.is_pack_container){
                    product.display_name = '■ ' + product.display_name;
                }
                if (options.is_pack_item){
                    product.display_name = '⁪├ ' + product.display_name;
                }
            }

            if(!product.is_pack || options.is_pack_container)
                return OrderSuper.prototype.addProduct.call(this, product, options);
        },

    });


/* ********************************************************
Overload : point_of_sale.Orderline

- Add extra behaviour when removing a pack
*********************************************************** */
    var OrderlineSuper = module.Orderline;
    module.Orderline = module.Orderline.extend({

        set_quantity: function(quantity){
            var self = this;
            var product = this.get_product();

            quantity = quantity || 'remove'
            if(quantity === 'remove'){

                if(product.is_pack_container || product.is_pack_item){

                    var o_lines = [];
                    var cur_order = this.pos.get('selectedOrder');
                    var sel_line = cur_order.selected_orderline;

                    (cur_order.get('orderLines')).each(_.bind( function(item) {
                        return o_lines.push(item);
                    }, this));

                    for(var i = 0,  len = o_lines.length; i < len; i++){
                        if (o_lines[i].get_product().pack_code == product.pack_code){
                            this.order.removeOrderline(o_lines[i]);
                        }
                    }

                }
                return OrderlineSuper.prototype.set_quantity.call(this, quantity);
            }else{
                // Deny changing quantity of pack or pack item
                if(!product.pack_code){
                    return OrderlineSuper.prototype.set_quantity.call(this, quantity);
                }
            }
        },

    });


/* ********************************************************
Overload : point_of_sale.PosWidget

- Create and append the new pack selection widget
*********************************************************** */
    module.PosWidget = module.PosWidget.extend({

        build_widgets: function(){
            this._super();

            this.product_pack_popup = new module.ProductPackPopup(this, {});
            this.product_pack_popup.appendTo($(this.$el));
            this.screen_selector.popup_set['product-pack-popup'] = this.product_pack_popup;
            this.product_pack_popup.hide();
        },

    });


};
