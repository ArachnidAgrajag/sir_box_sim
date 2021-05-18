from animate import Animate
from box_class import Box
if __name__ == "__main__":
    box1 = Box((10,10),(0,0))
    box1.add_people(100,0.1)
    box1.set_normal_dest()
    #box1.print_val()
    #box1.move_to_dest(0.3)
    #box1.update_infection(10)
    #box1.update_recovered(5)
    #box1.print_val() 
    anim1 = Animate(box1)
    anim1.run()