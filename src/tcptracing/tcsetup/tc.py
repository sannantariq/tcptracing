

class TC:
    def __init__(self, iface, mtu: int=1500) -> None:
        self.iface = iface
        self.mtu = mtu

    def config_mtu(self):
        """
        This function fixes the mtu of the interface to the value provided
        at input
        """
        pass

    def add_qdisc(self, parent, handle, qdisc_cmd):
        """
        This function adds a qdisc to the interface
        @input  parent:str
                handle:str
                qdisc_cmd:str
        """

        pass 

    def change_qdisc(self, parent, handle, qdisc_cmd):
        """
        This function changes a qdisc to the interface
        @input  parent:str
                handle:str
                qdisc_cmd:str
        """
        pass

    def delete_qdisc(self, parent, handle):
        """
        This function deletes a qdisc from the interface
        @input  parent:str
                handle:str
        """
        pass

    def add_class(self, parent, classid, class_cmd):
        """
        This function adds a class to a parent qdisc or class
        @input  parent:str
                classid:str
                class_cmd:str
        """

        pass 

    def change_class(self, parent, classid, class_cmd):
        """
        This function changes a class with parent qdisc or class
        @input  parent:str
                classid:str
                class_cmd:str
        """

        pass 

    def delete_class(self, parent, classid):
        """
        This function removes class to a parent qdisc or class
        @input  parent:str
                classid:str
        """

        pass 

    def add_filter(self, parent, prio, filter_cmd, leaf_flow_id):
        """
        This function adds a filter with priority prio to parent which
        maps traffic matching filter_cmd to leaf_flow_id class
        """
        pass

    def delete_filter(self, parent, prio):
        "This function removes all filters with priority prio"

        pass