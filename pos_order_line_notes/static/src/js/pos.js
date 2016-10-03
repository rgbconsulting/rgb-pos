/******************************************************************************
    Point Of Sale - Order Line Note
    See README file for full copyright and licensing details.
******************************************************************************/

openerp.pos_order_line_notes = function (instance) {
    module = instance.point_of_sale;
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;


/* ********************************************************
Overload: point_of_sale.PosWidget

- Add Notes PopUp 'NotesPopupWidget';
*********************************************************** */
    module.PosWidget = module.PosWidget.extend({

        build_widgets: function(){
            this._super();
            this.notes_popup = new module.NotesPopupWidget(this, {});
            this.notes_popup.appendTo($(this.$el));
            this.screen_selector.popup_set['notes-popup'] = this.notes_popup;

            // Hide popup by default
            this.notes_popup.hide();
        },
    });


/* ********************************************************
Define: pos_order_line_notes.NotesPopupWidget

- This widget displays a popup to create a note
*********************************************************** */
    module.NotesPopupWidget = module.PopUpWidget.extend({
        template:'NotesPopupWidget',

        start: function(){
            var self = this;

            // Add behaviour on Cancel Button
            this.$('#notes-popup-cancel').off('click').click(function(){
                self.clear();
                self.hide();
                self.pos.barcode_reader.connect();
            });

            // Add behaviour on Confirm Button
            this.$('#notes-popup-confirm').off('click').click(function(){
                self.confirm();
                self.clear();
                self.hide();
                self.pos.barcode_reader.connect();
            });
        },

        show: function(line){
            this.line = line;
            this.clear(line.note)
            this.pos.barcode_reader.disconnect();
            this._super();
            document.getElementById("note_text").select();
        },

        confirm: function(){
            var note = document.getElementById("note_text").value
            this.line.set_line_note(note);
            this.line.trigger('change', this.line);
        },

        clear: function(text){
            text = text || ""
            document.getElementById("note_text").value = text;
        }

    });


/* ********************************************************
Overload: point_of_sale.Orderline

- Define note field and set/get methods
*********************************************************** */
    var OrderlineSuper = module.Orderline;
    module.Orderline = module.Orderline.extend({

        initialize: function(attr, options) {
            this.note = null;
            OrderlineSuper.prototype.initialize.call(this, attr, options);
        },

        get_note: function(event) {
            return this.note;
        },

        set_line_note: function(value) {
            this.note = value;
        },

        export_as_JSON: function() {
            var res = OrderlineSuper.prototype.export_as_JSON.apply(this, arguments);
            res["line_note"] = this.note;
            return res;
        }

    });


/* ********************************************************
Overload: point_of_sale.Order

- Add event listener on note click
*********************************************************** */
    var OrderSuper = module.Order;
    module.Order = module.Order.extend({

        selectLine: function(line){
            self = this;
            OrderSuper.prototype.selectLine.call(this, line);

            // Show popup
            var el = document.getElementById('line_note');
            if(el != null){
                el.addEventListener('click', function(){
                    self.pos.pos_widget.screen_selector.show_popup('notes-popup', line);
                });
            }
        }

    });

}
