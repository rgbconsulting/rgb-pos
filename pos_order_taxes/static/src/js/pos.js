/******************************************************************************
    Point Of Sale - Taxes in POS Order
    See README file for full copyright and licensing details.
******************************************************************************/

openerp.pos_order_taxes = function (instance) {

    // Module initialization
    module = instance.point_of_sale;


/* ********************************************************
Extend: point_of_sale.Orderline

- Add display with taxes and taxes in export
*********************************************************** */
    var OrderlineSuper = module.Orderline;
    module.Orderline = module.Orderline.extend({

        get_display_price: function () {
            if (this.pos.config.display_price_with_taxes) {
                return this.get_price_with_tax();
            }
            return this.get_base_price();
        },

        get_display_unit_price: function(){
            if (this.pos.config.display_price_with_taxes) {
                return round_di(this.get_price_with_tax() / this.get_quantity(), this.pos.dp['Product Price']);
            }
            return round_di(this.price || 0, this.pos.dp['Product Price'])
        },

        export_for_printing: function(){
            var res = OrderlineSuper.prototype.export_for_printing.apply(this, arguments);
            res["product_price_with_tax"] = this.get_product().price_with_taxes
            return res;
        },

        export_as_JSON: function() {
            var res = OrderlineSuper.prototype.export_as_JSON.apply(this, arguments);
            var product_tax_ids = this.get_product().taxes_id || [];
            res["tax_ids"] = [[6, false, product_tax_ids]];
            return res;
        }

    });


/* ********************************************************
Extend: point_of_sale.ProductListWidget

- Add display_price_with_taxes for the product template
*********************************************************** */
    instance.point_of_sale.ProductListWidget.include({
        init: function (parent, options) {
            this._super(parent, options);
            this.display_price_with_taxes = false;
            if (
                posmodel
                && posmodel.config
                && posmodel.config.display_price_with_taxes
            ) {
                this.display_price_with_taxes
                    = posmodel.config.display_price_with_taxes
            }
        }
    });


/* ********************************************************
Extend: point_of_sale.PosDB

- Store price with taxes of each product
*********************************************************** */
    module.PosDB = module.PosDB.extend({
        add_products: function (products) {
            this._super(products);
            var pos = posmodel.pos_widget.pos;
            for (var id in this.product_by_id) {
                if (this.product_by_id.hasOwnProperty(id)) {
                    var product = this.product_by_id[id];
                    var orderline = new openerp.point_of_sale.Orderline({}, {
                        pos: pos,
                        order: null,
                        product: product,
                        price: product.price
                    });
                    var prices = orderline.get_all_prices();
                    this.product_by_id[id].price_with_taxes
                        = prices['priceWithTax']
                }
            }
        },

    });

};
