class RoomType:
    def __init__(self, category, num_people, cost, cost_extra_bed):
        self.num_people = num_people
        self.category = category
        self.cost = cost
        self.cost_extra_bed = cost_extra_bed

    def get_num_people(self):
        return self.num_people

    def get_category(self):
        return self.category

    def get_cost(self):
        return self.cost

    def get_cost_extra_bed(self):
        return self.cost_extra_bed