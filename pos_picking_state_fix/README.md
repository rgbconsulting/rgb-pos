RGB POS Picking State Fix
=========================

This module fixes the pickings created from POS orders, passing them
to *Waiting Availability* state if the state is not *Transferred*.

This fix was made in order to avoid stock errors when selling products
with *lots* inside the Point Of Sale.

Credits
=======

License
-------

* [GNU Affero General Public License] (http://www.gnu.org/licenses/agpl.html)

Author
------

* Copyright, RGB Consulting SL (www.rgbconsulting.com)

Contributors
------------

* RGB Consulting SL <odoo@rgbconsulting.com>
