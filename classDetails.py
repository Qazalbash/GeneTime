class ClassDetails:
    def __init__(self) -> None:
        self.Class_Dict = {}

    def addClass(self, classNbr, day, room, start_time, end_time):
        self.Class_Dict[classNbr] = self.Class_Dict.get(classNbr, []) + [[day, room, start_time,
                                                                          end_time]]

    def getInfo(self, classNbr):
        return self.Class_Dict[classNbr]
