/******************************************************************************
    Point Of Sale - Multiple Scales for POS
    See README file for full copyright and licensing details.
******************************************************************************/

openerp.pos_scale_multi = function(instance){

    module = instance.point_of_sale;


/* ********************************************************
Overload: point_of_sale.PosModel

- Load scale configuration and parameters
*********************************************************** */
    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
        self = this;

        model = {
            model: 'pos.scale.config',
            fields: [
                'name',
                'driver',
                'params_ids',
            ],
            loaded: function(self, values){
                self.db.add_scale_config(values);
            },
        }
        this.models.push(model);

        model = {
            model: 'pos.scale.config.params',
            fields: [
                'name',
                'value',
            ],
            loaded: function(self, values){
                self.db.add_scale_config_params(values);
            },
        }
        this.models.push(model);

        _initialize_.call(this, session, attributes);

    };


/* ********************************************************
Extend: point_of_sale.PosDB

- Store the new loaded data
*********************************************************** */
    module.PosDB = module.PosDB.extend({

        init: function(options){
            this.pos_scale_configs = {};
            this.pos_scale_config_params = {};
            this._super(options);
        },

        add_scale_config: function(configs){
            for(var i=0 ; i < configs.length ; i++){
                this.pos_scale_configs[configs[i].id] = configs[i];
            }
        },

        add_scale_config_params: function(params){
            for(var i=0 ; i < params.length ; i++){
                this.pos_scale_config_params[params[i].id] = params[i];
            }
        }

    });


/* ********************************************************
Extend: point_of_sale.ProxyDevice

- Add method to send scale configuration
*********************************************************** */
    module.ProxyDevice = module.ProxyDevice.extend({

        send_scale_config: function(){
            var config_id = this.pos.config.iface_scale_config[0];
            var params = {}
            var driver = this.pos.db.pos_scale_configs[config_id].driver;
            var param_ids = this.pos.db.pos_scale_configs[config_id].params_ids;

            for(var i=0;  i < param_ids.length; i++){
                var param = this.pos.db.pos_scale_config_params[param_ids[i]];
                params[param.name] = param.value
            }

            params['driver'] = driver;
            return this.message('scale_config', {'params':JSON.stringify(params)});
        },

    });


/* ********************************************************
Extend: point_of_sale.PosModel

- Call scale configuration method
*********************************************************** */
    var PosModelSuper = module.PosModel;
    module.PosModel = module.PosModel.extend({

        connect_to_proxy: function(){
            var self = this;
            var res = PosModelSuper.prototype.connect_to_proxy.call(this);

            res = res.then(function(){
                if(self.config.iface_scale_config && self.config.iface_electronic_scale){
                    self.proxy.send_scale_config()
                }
            })

            return res;
        },

    });


};
