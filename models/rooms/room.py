class Room:
    def __init__(self, num_people, category, cost, cost_extra_bed, room_num, location):
        self.num_people = num_people
        self.category = category
        self.cost = cost
        self.cost_extra_bed = cost_extra_bed
        self.room_num = room_num
        self.location = location

    def get_num_people(self):
        return self.num_people

    def get_category(self):
        return self.category

    def get_cost(self):
        return self.cost

    def get_cost_extra_bed(self):
        return self.cost_extra_bed

    def get_room_num(self):
        return self.room_num

    def get_location(self):
        return self.location
