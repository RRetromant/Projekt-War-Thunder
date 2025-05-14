import csv

class Airplane:
    def __init__(self, nation, name, battlerating, plane_type, turnrate, climbrate, speed, speedheight, maxheight):
        self.nation = nation
        self.name = name
        self.battlerating = battlerating
        self.plane_type = plane_type
        self.turnrate = turnrate
        self.climbrate = climbrate
        self.speed = speed
        self.speedheight = speedheight
        self.maxheight = maxheight

class Armament: #Beinhaltet dumb Bombs, retarded Bombs, und dumb Rockets
    def __init__(self, armament_type, projectile_mass, explosive_type, explosive_mass, TNT_equivalent):
        self.armament_type = armament_type
        self. projectile_mass = projectile_mass
        self.explosive_type = explosive_type
        self.explosive_mass = explosive_mass
        self.TNT_equivalent = TNT_equivalent

#Die nächsten drei Klassen erben die Stats von Armament:
class WeaponGuided(Armament): #beinhaltet Guided Bombs. neuer Stat: Guidance, Missile-guidance-time
    def __init__(self, armament_type, projectile_mass, explosive_type, explosive_mass, TNT_equivalent, guidance, missile_guidance_time):
        super().__init__(armament_type, projectile_mass, explosive_type, explosive_mass, TNT_equivalent)
        self.guidance = guidance
        self.missile_guidance_time = missile_guidance_time

class AirToGroundRocketGuided(WeaponGuided): #neuer Stat: Launch range, maxSpeed
    def __init__(self, armament_type, projectile_mass, explosive_type, explosive_mass, TNT_equivalent, guidance, missile_guidance_time, launch_range, maxspeed):
        super().__init__(armament_type, projectile_mass, explosive_type, explosive_mass, TNT_equivalent, guidance, missile_guidance_time)
        self.launch_range = launch_range
        self.maxspeed = maxspeed
        
class AirToAirRocket(AirToGroundRocketGuided): #neuer Stat:  Aspect, Lock-Range, Lock-Range-rear, maxG-Overload
    def __init__(self, armament_type, projectile_mass, explosive_type, explosive_mass, TNT_equivalent, guidance, missile_guidance_time, launch_range, maxspeed, aspect, lock_range, lock_range_rear, maxg_overload):
        super().__init__(armament_type, projectile_mass, explosive_type, explosive_mass, TNT_equivalent, guidance, missile_guidance_time, launch_range, maxspeed)
        self.aspect = aspect
        self.lock_range = lock_range
        self.lock_range_rear = lock_range_rear
        self.maxg_overload = maxg_overload
