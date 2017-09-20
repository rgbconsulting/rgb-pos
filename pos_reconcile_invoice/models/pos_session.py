# -*- coding: utf-8 -*-
# See README file for full copyright and licensing details.

from openerp import models, api


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.multi
    def _confirm_orders(self):
        res = super(PosSession, self)._confirm_orders()
        # Check if auto reconcile is activated for this pos config
        if not self.config_id.iface_auto_reconcile:
            return res

        aml_reconcile_model = self.env['account.move.line.reconcile']
        default_account = self.env['ir.property'].get('property_account_receivable', 'res.partner')

        for order in self.order_ids.filtered(lambda rec: rec.state == 'invoiced'):
            # Check invoice state
            invoice = order.invoice_id
            if not invoice or invoice.state not in ('draft', 'open'):
                continue
            if invoice.state == 'draft':
                invoice.signal_workflow('invoice_open')

            # Find order account
            current_company = order.sale_journal.company_id
            order_account = (
                order.partner_id and
                order.partner_id.property_account_receivable and
                order.partner_id.property_account_receivable.id or
                default_account and default_account.id or
                current_company.account_receivable.id
            )

            lines = []
            # Get payment lines
            for statement in order.statement_ids:
                if statement.account_id.id != order_account:
                    continue

                for line in statement.journal_entry_id.line_id:
                    if line.account_id.id == order_account and line.state == 'valid':
                        lines.append(line.id)

            # Get invoice line
            commercial_partner = order.partner_id.commercial_partner_id.id
            for line in invoice.move_id.line_id:
                if (line.partner_id.id == commercial_partner and
                        line.account_id.id == order_account and
                        line.state == 'valid'):
                    lines.append(line.id)
                    break

            # Reconcile invoice
            context_cpy = self._context.copy()
            context_cpy.update({'active_ids': lines})
            aml_reconcile_model.with_context(context_cpy).trans_rec_reconcile_full()
        return res
