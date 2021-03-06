#//
#//-----------------------------------------------------------------------------
#//   Copyright 2007-2011 Mentor Graphics Corporation
#//   Copyright 2007-2011 Cadence Design Systems, Inc.
#//   Copyright 2010 Synopsys, Inc.
#//   Copyright 2013 NVIDIA Corporation
#//   Copyright 2019-2020 Tuomas Poikela (tpoikela)
#//   All Rights Reserved Worldwide
#//
#//   Licensed under the Apache License, Version 2.0 (the
#//   "License"); you may not use this file except in
#//   compliance with the License.  You may obtain a copy of
#//   the License at
#//
#//       http://www.apache.org/licenses/LICENSE-2.0
#//
#//   Unless required by applicable law or agreed to in
#//   writing, software distributed under the License is
#//   distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#//   CONDITIONS OF ANY KIND, either express or implied.  See
#//   the License for the specific language governing
#//   permissions and limitations under the License.
#//-----------------------------------------------------------------------------

from .uvm_object import UVMObject
from uvm.macros import *

#// File: UVM Links
#//
#// The <UVMLinkBase> class, and its extensions, are provided as a mechanism
#// to allow for compile-time safety when trying to establish links between
#// records within a <uvm_tr_database>.
#//
#//

#//------------------------------------------------------------------------------
#//
#// CLASS: UVMLinkBase
#//
#// The ~UVMLinkBase~ class presents a simple API for defining a link between
#// any two objects.
#//
#// Using extensions of self class, a <uvm_tr_database> can determine the
#// type of links being passed, without relying on "magic" string names.
#//
#// For example:
#// |
#// | virtual def void do_establish_link(self,UVMLinkBase link):
#// |   UVMParentChildLink pc_link
#// |   UVMCauseEffectLink ce_link
#// |
#// |   if (sv.cast(pc_link, link)):
#// |      // Record the parent-child relationship
#// |   end
#// |   elif (sv.cast(ce_link, link)):
#// |      // Record the cause-effect relationship
#// |   end
#// |   else begin
#// |      // Unsupported relationship!
#// |   end
#// | endfunction : do_establish_link
#//

class UVMLinkBase(UVMObject):


    def __init__(self, name="unnamed-UVMLinkBase"):
        """         
           Function: new
           Constructor
          
           Parameters:
           name - Instance name
        Args:
            name: 
        """
        super().__init__(name)

    def set_lhs(self, lhs):
        """         
           Group:  Accessors

           Function: set_lhs
           Sets the left-hand-side of the link
          
           Triggers the `do_set_lhs` callback.
        Args:
            lhs: 
        """
        self.do_set_lhs(lhs)

    def get_lhs(self):
        """         
           Function: get_lhs
           Gets the left-hand-side of the link
          
           Triggers the `do_get_lhs` callback
        Returns:
        """
        return self.do_get_lhs()

    def set_rhs(self, rhs):
        """         
           Function: set_rhs
           Sets the right-hand-side of the link
          
           Triggers the `do_set_rhs` callback.
        Args:
            rhs: 
        """
        self.do_set_rhs(rhs)


    def get_rhs(self):
        """         
           Function: get_rhs
           Gets the right-hand-side of the link
          
           Triggers the `do_get_rhs` callback
        Returns:
        """
        return self.do_get_rhs()


    def set(self, lhs, rhs):
        """         
           Function: set
           Convenience method for setting both sides in one call.
          
           Triggers both the `do_set_rhs` and `do_set_lhs` callbacks.
        Args:
            lhs: 
            rhs: 
        """
        self.do_set_lhs(lhs)
        self.do_set_rhs(rhs)


    #   // Group: Implementation Callbacks
    #
    #   // Function: do_set_lhs
    #   // Callback for setting the left-hand-side
    #   pure virtual def void do_set_lhs(self,UVMObject lhs):
    #
    #   // Function: do_get_lhs
    #   // Callback for retrieving the left-hand-side
    #   pure virtual def UVMObject do_get_lhs(self):
    #
    #   // Function: do_set_rhs
    #   // Callback for setting the right-hand-side
    #   pure virtual def void do_set_rhs(self,UVMObject rhs):
    #
    #   // Function: do_get_rhs
    #   // Callback for retrieving the right-hand-side
    #   pure virtual def UVMObject do_get_rhs(self):
    #
    #endclass : UVMLinkBase

#//------------------------------------------------------------------------------
#//
#// CLASS: UVMParentChildLink
#//
#// The ~UVMParentChildLink~ is used to represent a Parent/Child relationship
#// between two objects.
#//


class UVMParentChildLink(UVMLinkBase):

    def __init__(self, name="unnamed-UVMParentChildLink"):
        """         
           Function: new
           Constructor
          
           Parameters:
           name - Instance name
        Args:
            name: 
        """
        super().__init__(name)
        self.m_lhs = None
        self.m_rhs = None


    @classmethod
    def get_link(cls, lhs, rhs, name="pc_link"):
        """         
           Function: get_link
           Constructs a pre-filled link
          
           This allows for simple one-line link creations.
        .. code-block:: python

           | my_db.establish_link(UVMParentChildLink::get_link(record1, record2))
          
           Parameters:
           lhs - Left hand side reference
           rhs - Right hand side reference
           name - Optional name for the link object
          
        Args:
            cls: 
            lhs: 
            rhs: 
            name: 
        Returns:
        """
        pc_link = UVMParentChildLink(name)
        pc_link.set(lhs, rhs)
        return pc_link


    def do_set_lhs(self, lhs):
        """         
           Group: Implementation Callbacks

           Function: do_set_lhs
           Sets the left-hand-side (Parent)
          
        Args:
            lhs: 
        """
        self.m_lhs = lhs

    def do_get_lhs(self):
        """         
           Function: do_get_lhs
           Retrieves the left-hand-side (Parent)
          
        Returns:
        """
        return self.m_lhs

    def do_set_rhs(self, rhs):
        """         
           Function: do_set_rhs
           Sets the right-hand-side (Child)
          
        Args:
            rhs: 
        """
        self.m_rhs = rhs


    def do_get_rhs(self):
        """         
           Function: do_get_rhs
           Retrieves the right-hand-side (Child)
          
        Returns:
        """
        return self.m_rhs

    #
    #endclass : UVMParentChildLink



#//------------------------------------------------------------------------------
#//
#// CLASS: UVMCauseEffectLink
#//
#// The ~UVMCauseEffectLink~ is used to represent a Cause/Effect relationship
#// between two objects.
#//


class UVMCauseEffectLink(UVMLinkBase):

    #   // Variable- m_lhs,m_rhs
    #   // Implementation details
    #   local UVMObject m_lhs
    #   local UVMObject m_rhs


    def __init__(self, name="unnamed-UVMCauseEffectLink"):
        """         
           Function: new
           Constructor
          
           Parameters:
           name - Instance name
        Args:
            name: 
        """
        super().__init__(name)


    @classmethod
    def get_link(cls, lhs, rhs, name="ce_link"):
        """         
           Function: get_link
           Constructs a pre-filled link
          
           This allows for simple one-line link creations.
        .. code-block:: python

           | my_db.establish_link(UVMCauseEffectLink::get_link(record1, record2))
          
           Parameters:
           lhs - Left hand side reference
           rhs - Right hand side reference
           name - Optional name for the link object
          
        Args:
            cls: 
            lhs: 
            rhs: 
            name: 
        Returns:
        """
        ce_link = UVMCauseEffectLink(name)
        ce_link.set(lhs, rhs)
        return ce_link


    def do_set_lhs(self, lhs):
        """         
           Group: Implementation Callbacks

           Function: do_set_lhs
           Sets the left-hand-side (Cause)
          
        Args:
            lhs: 
        """
        self.m_lhs = lhs


    def do_get_lhs(self):
        """         
           Function: do_get_lhs
           Retrieves the left-hand-side (Cause)
          
        Returns:
        """
        return self.m_lhs


    def do_set_rhs(self, rhs):
        """         
           Function: do_set_rhs
           Sets the right-hand-side (Effect)
          
        Args:
            rhs: 
        """
        self.m_rhs = rhs


    def do_get_rhs(self):
        """         
           Function: do_get_rhs
           Retrieves the right-hand-side (Effect)
          
        Returns:
        """
        return self.m_rhs

uvm_object_utils(UVMParentChildLink)

#//------------------------------------------------------------------------------
#//
#// CLASS: UVMRelatedLink
#//
#// The ~UVMRelatedLink~ is used to represent a generic "is related" link
#// between two objects.
#//


class UVMRelatedLink(UVMLinkBase):


    def __init__(self, name="unnamed-UVMRelatedLink"):
        """         
           Function: new
           Constructor
          
           Parameters:
           name - Instance name
        Args:
            name: 
        """
        super().__init__(name)
        self.m_lhs = None  # type: UVMObject
        self.m_rhs = None  # type: UVMObject


    @classmethod
    def get_link(cls, lhs, rhs, name="ce_link"):
        """         
           Function: get_link
           Constructs a pre-filled link
          
           This allows for simple one-line link creations.
        .. code-block:: python

           | my_db.establish_link(UVMRelatedLink::get_link(record1, record2))
          
           Parameters:
           lhs - Left hand side reference
           rhs - Right hand side reference
           name - Optional name for the link object
          
        Args:
            cls: 
            lhs: 
            rhs: 
            name: 
        Returns:
        """
        ce_link = UVMRelatedLink(name)
        ce_link.set(lhs, rhs)
        return ce_link


    #   // Group: Implementation Callbacks
    #
    #   // Function: do_set_lhs
    #   // Sets the left-hand-side
    #   //
    #   virtual def void do_set_lhs(self,UVMObject lhs):
    #      m_lhs = lhs
    #   endfunction : do_set_lhs

    #   // Function: do_get_lhs
    #   // Retrieves the left-hand-side
    #   //
    #   virtual def UVMObject do_get_lhs(self):
    #      return m_lhs
    #   endfunction : do_get_lhs

    #   // Function: do_set_rhs
    #   // Sets the right-hand-side
    #   //
    #   virtual def void do_set_rhs(self,UVMObject rhs):
    #      m_rhs = rhs
    #   endfunction : do_set_rhs

    #   // Function: do_get_rhs
    #   // Retrieves the right-hand-side
    #   //
    #   virtual def UVMObject do_get_rhs(self):
    #      return m_rhs
    #   endfunction : do_get_rhs


uvm_object_utils(UVMRelatedLink)
