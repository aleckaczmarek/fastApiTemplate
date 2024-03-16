from system.util.DomainInterface import DomainModel

class AiModel(DomainModel):
    question:  str = None

    def __eq__(self, other):
        return super().__eq__() and self.question == other.question
     
