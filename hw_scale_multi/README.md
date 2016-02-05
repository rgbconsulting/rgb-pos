RGB Scale Multi Hardware Driver
===============================

This module replaces the standard *hw_scale* module to add new scale drivers.

Features
--------

* A scale configuration controller 
* An abstract driver that can be extended to define new scale drivers
* Drivers for the *Dibal* and *Mettler* scales

Installation
------------

This module is not designed to work with the standard *hw_scale* module,
therefore the *hw_scale* module should be uninstalled prior to the
installation of this one.

This module is designed to be installed on the *PosBox*.
On the *main Odoo server*, you should install the module *pos_scale_multi*.

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
