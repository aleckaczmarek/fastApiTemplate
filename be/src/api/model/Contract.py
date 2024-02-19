from typing import Optional,List

from system.util.DomainInterface import DomainModel

class Contract(DomainModel):
    collection_name:Optional[str]  = "contracts"
    total:Optional[str]

    def __eq__(self, other):
        return super().__eq__() and self.total == other.total
 
     
