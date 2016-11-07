# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID, api, models


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    @api.multi
    def _merge(self, partner_ids, dst_partner=None):
        """Allow non-admins to merge partners with different emails."""
        # Know if user has unrestricted access
        group_unrestricted = self.env["ir.model.data"].xmlid_to_object(
            "crm_deduplicate_acl.group_unrestricted")

        # Run as admin if so
        return super(BasePartnerMergeAutomaticWizard, self)._merge(
            self.env.cr,
            SUPERUSER_ID if group_unrestricted.id
                            in self.env.user.groups_id.ids else self.env.uid,
            partner_ids=partner_ids,
            dst_partner=dst_partner,
            context=self.env.context)
