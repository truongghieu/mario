class boss_manager:
    def __init__ (self,enable=True):
        
        self.bosses = []
        self.boss_active = 0
        self.boss_timer_active = []
        self.enable = enable

    def render(self,display,offset=(0,0)):
        if self.enable:
            for boss in self.bosses:
                if boss.enable:
                    boss.render(display,offset)
    def update(self):
        if self.enable:
            for boss in self.bosses:
                boss.update()

    def add_boss(self,boss):
        self.bosses.append(boss)
    def remove_boss(self,boss):
        self.bosses.remove(boss)    
    def wake_up_boss(self,index = 0):
        self.bosses[index].enable = True


    def reset(self):
        for boss in self.bosses:
            boss.enable = False
            self.boss_active = 0
            for i in range(len(self.bosses)):
                self.bosses[i].health = int( (i+1) * 20 )                
            # boss.position = boss.defaut_pos
            boss.image.reset()