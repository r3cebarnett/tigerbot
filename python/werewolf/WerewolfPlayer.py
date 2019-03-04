import asyncio

class WerewolfPlayer:
    def __init__(self, id):
        self.id = id
        self.role = None
        self.command = None
        self.ready = False

    def setRole(self, role):
        self.role = role
        self.command = getattr(WerewolfRoles, role)

    def villager(self):

    def werewolf(self):

    def tanner(self):

    def mason(self):

    def robber(self):

    def troublemaker(self):

    def seer(self):

    def appr_seer(self):

    def witch(self):

    def para_inv(self):

    def drunk(self):

    def vill_idiot(self):

    def insomniac(self):

    def revealer(self):

    def aura_seer(self):

    def alpha_wolf(self):

    def mystic_wolf(self):

    def dream_wolf(self):

    def minion(self):
