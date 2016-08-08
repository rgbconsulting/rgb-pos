/******************************************************************************
    Point Of Sale - POS Cache Enhanced
    See README file for full copyright and licensing details.
******************************************************************************/

openerp.pos_cache_enhanced = function (instance) {
    module = instance.point_of_sale;
    var _t = instance.web._t;

    var posmodel_super = module.PosModel.prototype;
    module.PosModel = module.PosModel.extend({

        handleCodePoints: function (array) {
            var CHUNK_SIZE = 60000;
            var index = 0;
            var length = array.length;
            var result = '';
            var slice;
            while (index < length) {
                slice = array.slice(index, Math.min(index + CHUNK_SIZE, length));
                result += String.fromCharCode.apply(null, slice);
                index += CHUNK_SIZE;
            }
            return result;
        },

        load_server_data: function () {
            var self = this;

            var product_index = -1;
            for (var i = 0 ; i < this.models.length; i++){
                if (this.models[i].model == 'product.product'){
                    product_index = i;
                }
            }

            var product_model = this.models[product_index];
            var product_fields = product_model.fields;
            var product_domain = product_model.domain;

            if (product_index !== -1) {
                this.models.splice(product_index, 1);
            }

            return posmodel_super.load_server_data.apply(this, arguments).then(function () {
                var records = new instance.web.Model('pos.config').call('get_products_from_cache',
                                                           [self.pos_session.config_id[0], product_fields, product_domain]);

                self.pos_widget.loading_message(_t('Loading products'))
                return records.then(function (products) {
                    products = window.atob(products)
                    products = products.split('').map(function(x){return x.charCodeAt(0);});
                    products = new Uint8Array(products);
                    products = pako.inflate(products);
                    products = new Uint16Array(products)
                    products = self.handleCodePoints(products)
                    self.db.add_products(eval(products));
                });
            });
        },
    });
};
