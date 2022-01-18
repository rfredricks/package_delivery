from datetime import datetime
from datetime import timedelta
# truck represents truck carrying packages
class Truck:

    # constructor
    def __init__(self, truck_num, mileage, curr_time):
        self.truck_num = truck_num
        self.mileage = (float(mileage))
        self.curr_time = datetime.strptime(curr_time, '%H:%M:%S')
        self.packages = []

    # load list of packages onto the truck
    def load(self, item):
        self.packages.append(item)

    # add mileage. update time at the rate of 18 mph
    def update_mileage(self, miles):
        self.mileage += (float(miles))
        delta = float(miles * 10 / 3)  # time is at 18 mph - converted to minutes
        self.curr_time += timedelta(minutes=delta)

    # deliver package, remove from truck list
    def deliver(self, package):
        package[8] = 'Delivered at ' + self.curr_time.strftime('%H:%M:%S')  # update delivery status
        self.packages.remove(package)  # remove package from truck list
        return package  # return updated package
