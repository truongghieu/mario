import random 
class zombie_manager:
    def __init__ (self,zombie,zombie_count=2,zombie_spawn_time=200,enable=True):
        self.zombie = zombie
        self.spawn_positions =[[45,40],[125,40],[205,40],[75,90], [175,90],[45,140],[125,140],[205,140]]
        self.zombies = []
        self.zombie_count = zombie_count
        self.zombie_spawn_time = zombie_spawn_time
        self.current_time = zombie_spawn_time
        self.enable = enable
        for spawn in self.spawn_positions:
            self.zombies.append(self.zombie.copy())
            self.zombies[-1].position = spawn
            self.zombies[-1].enable = False        
    def update(self):
        if self.enable:
            if self.timer():
                self.enable_random()
            for zombie in self.zombies:
                zombie.update()
        else:
            for zombie in self.zombies:
                zombie.enable = False
                



    def render(self,display,offset=(0,0)):
        for zombie in self.zombies:
            zombie.render(display,offset)

    def timer(self):
        self.current_time -= 1
        if self.current_time <= 0:
            self.current_time = self.zombie_spawn_time
            return True
        return False
    def enable_random(self):
        for i in range(self.zombie_count):
            temp = random.randint(0,len(self.zombies)-1)
            self.zombies[temp].enable = True
            



        