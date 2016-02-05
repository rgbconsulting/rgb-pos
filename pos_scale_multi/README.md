RGB POS Scale Multi
===================

This module adds support for multiple scales in the Point of Sale.

Installation
------------

This module is designed to be installed on the *main Odoo server*.
On the *PosBox*, you should install the module *hw_scale_multi*.

Configuration
-------------

This module currently supports two types of scales: *Mettler* and *Dibal*.
The scales can be configured on the main Odoo server, in the menu *Point
of Sale > Configuration > Scales*.

The serial port parameters (baudrate, bytesize, stopbits, parity, timeout, 
device_path) can be defined for both scales.

For the *Dibal* scale, the following extra parameters can be defined:

- *read_weight*: the weight reading command
- *weight_start_integer*: the position where the whole weight starts
- *weight_integer*: the whole weight size
- *weight_start_decimal*: the position where the decimal weight starts
- *weight decimal*: the decimal weight size

Usage
-----

In the POS configuration, when enabling electronic scale, the scale
configuration to be used in the Pos can be specified.

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
