class ClassDetails:
    def __init__(self) -> None:
        # self.info =[]
        self.Class_Dict = {}

    def addClass(self, classNbr, day, room, start_time, end_time):
        self.Class_Dict[classNbr] = self.Class_Dict.get(classNbr, []) + [[day, room, start_time,
                                                                          end_time]]  # if classNbr in self.Class_Dict:  #     self.Class_Dict[classNbr].append([day, room, start_time, end_time])  # else:  #     self.Class_Dict[classNbr] = [[day, room, start_time, end_time]]

    def getInfo(self, classNbr):
        return self.Class_Dict[classNbr]
